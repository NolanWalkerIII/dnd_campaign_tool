"""
Discord bot for D&D Campaign Manager.

Runs alongside Flask in a background thread. Provides slash commands
for players and DMs, rich embeds for character sheets and combat,
and bridges SMS ↔ Discord so both channels see the same game.

Env vars:
  DISCORD_BOT_TOKEN  — Bot token from Discord Developer Portal
"""
import asyncio
import os
import threading
from datetime import datetime

import discord
from discord import app_commands

# ── Bot setup ────────────────────────────────────────────────

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True


class DnDBot(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        # Don't sync globally here — it blocks for minutes.
        # Commands get synced per-guild in on_ready and on_guild_join.
        pass

    async def on_ready(self):
        print(f'[Discord] Bot connected as {self.user} (ID: {self.user.id})', flush=True)
        print(f'[Discord] Invite URL: {invite_url()}', flush=True)
        print(f'[Discord] Guilds: {[g.name for g in self.guilds]}', flush=True)
        # Sync commands to each guild the bot is already in
        for guild in self.guilds:
            try:
                self.tree.copy_global_to(guild=guild)
                await self.tree.sync(guild=guild)
                print(f'[Discord] Synced commands to {guild.name}', flush=True)
            except Exception as e:
                print(f'[Discord] Failed to sync to {guild.name}: {e}', flush=True)

    async def on_guild_join(self, guild):
        """Sync slash commands when bot joins a new server."""
        print(f'[Discord] Joined guild: {guild.name}', flush=True)
        try:
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
            print(f'[Discord] Synced commands to {guild.name}', flush=True)
        except Exception as e:
            print(f'[Discord] Failed to sync to {guild.name}: {e}', flush=True)


bot = DnDBot()
_flask_app = None
_bot_loop = None

CLASS_COLORS = {
    'Fighter':   0xE74C3C,
    'Wizard':    0x3498DB,
    'Rogue':     0x2ECC71,
    'Cleric':    0xF1C40F,
    'Ranger':    0x27AE60,
    'Paladin':   0xE67E22,
    'Barbarian': 0xE91E63,
    'Bard':      0x9B59B6,
    'Druid':     0x1ABC9C,
    'Monk':      0x95A5A6,
    'Sorcerer':  0xC0392B,
    'Warlock':   0x8E44AD,
}

DM_COLOR = 0xC9A84C      # gold
COMBAT_COLOR = 0xE94560   # accent red
SUCCESS_COLOR = 0x4CAF8A  # green


# ── Database helpers (run inside Flask app context) ──────────

def _get_campaign_for_guild(guild_id):
    """Find the campaign linked to a Discord guild."""
    from models import Campaign
    for c in Campaign.query.filter(Campaign.is_active == True).all():
        state = c.current_state or {}
        if str(state.get('discord', {}).get('guild_id')) == str(guild_id):
            return c
    return None


def _get_player_context(guild_id, discord_user_id):
    """Get (campaign, character, user) for a Discord user."""
    from models import User, Character
    user = User.query.filter_by(discord_id=str(discord_user_id)).first()
    if not user:
        return None, None, None
    campaign = _get_campaign_for_guild(guild_id)
    if not campaign:
        return None, None, None
    if user.id not in (campaign.players or []) and campaign.dm_id != user.id:
        return None, None, None
    char = Character.query.filter_by(user_id=user.id, campaign_id=campaign.id).first()
    if not char:
        char = Character.query.filter_by(user_id=user.id).first()
    return campaign, char, user


def _is_dm(guild_id, discord_user_id):
    """Check if a Discord user is the DM for the campaign in this guild."""
    from models import User
    campaign = _get_campaign_for_guild(guild_id)
    if not campaign:
        return False, None
    dm = User.query.get(campaign.dm_id)
    if dm and str(dm.discord_id) == str(discord_user_id):
        return True, campaign
    return False, None


def _get_tavern_channel(campaign):
    """Get the tavern channel ID for a campaign."""
    state = campaign.current_state or {}
    return state.get('discord', {}).get('channels', {}).get('tavern')


# ── Embed builders ──────────────────────────────────────────

def character_embed(char):
    """Rich embed for a character sheet."""
    from services.engine import ability_modifier, mod_str
    scores = char.ability_scores or {}
    color = CLASS_COLORS.get(char.class_name, 0x808080)

    em = discord.Embed(
        title=f"⚔ {char.name}",
        description=f"Level {char.level} {char.race} {char.class_name}",
        color=color,
    )

    # Stats
    stat_lines = []
    for ab in ['STR', 'DEX', 'CON', 'INT', 'WIS', 'CHA']:
        s = scores.get(ab, 10)
        m = ability_modifier(s)
        stat_lines.append(f"**{ab}** {s} ({mod_str(m)})")
    em.add_field(name="Ability Scores", value="\n".join(stat_lines), inline=True)

    # Combat stats
    hp_bar = _hp_bar(char.hp_current, char.hp_max)
    combat_info = (
        f"**HP** {char.hp_current}/{char.hp_max} {hp_bar}\n"
        f"**AC** {char.ac}\n"
        f"**Prof** +{char.proficiency_bonus}"
    )
    em.add_field(name="Combat", value=combat_info, inline=True)

    # Skills
    skills = char.skills or []
    if skills:
        em.add_field(name="Proficiencies", value=", ".join(skills), inline=False)

    # Equipment (first 8)
    equip = char.equipment or []
    if equip:
        em.add_field(name="Equipment", value=", ".join(equip[:8]), inline=False)

    # Spells
    spells_data = char.spells or {}
    known = spells_data.get('known', [])
    if known:
        em.add_field(name="Spells", value=", ".join(known), inline=False)

    return em


def combat_embed(campaign):
    """Rich embed showing the current combat state."""
    state = campaign.current_state or {}
    order = state.get('initiative_order', [])
    turn_idx = state.get('turn_index', 0)
    round_num = state.get('round', 1)

    em = discord.Embed(
        title=f"⚔ COMBAT — Round {round_num}",
        color=COMBAT_COLOR,
    )

    if not order:
        em.description = "No combatants. Use `/npc add` to add enemies."
        return em

    lines = []
    for i, entry in enumerate(order):
        marker = "▸ " if i == turn_idx else "  "
        name = entry['name']
        init = entry['initiative']

        if entry.get('is_npc') and entry.get('npc_hp') is not None:
            hp_bar = _hp_bar(entry['npc_hp'], entry['npc_hp_max'])
            hp_str = f" {entry['npc_hp']}/{entry['npc_hp_max']} {hp_bar}"
        else:
            hp_str = ""

        bold = "**" if i == turn_idx else ""
        lines.append(f"{marker}{bold}{name}{bold} (Init {init}){hp_str}")

    em.description = "\n".join(lines)

    current = order[turn_idx] if turn_idx < len(order) else None
    if current:
        em.set_footer(text=f"It's {current['name']}'s turn!")

    return em


def roll_embed(char_name, result_text, action_type='roll'):
    """Embed for a dice roll result."""
    color = COMBAT_COLOR if action_type == 'attack' else DM_COLOR
    em = discord.Embed(description=f"🎲 **{char_name}**: {result_text}", color=color)
    return em


def narration_embed(text, dm_name="AI DM"):
    """Embed for DM narration."""
    em = discord.Embed(description=text, color=DM_COLOR)
    em.set_author(name=f"📜 {dm_name}")
    return em


def _hp_bar(current, maximum, length=10):
    if not maximum:
        return ""
    pct = max(0, current / maximum)
    filled = round(pct * length)
    return "▓" * filled + "░" * (length - filled)


# ── Core action processor ───────────────────────────────────

async def process_discord_action(interaction, text):
    """Process a player action through the AI DM pipeline."""
    await interaction.response.defer()

    def _do():
        campaign, char, user = _get_player_context(
            interaction.guild_id, interaction.user.id
        )
        if not campaign or not char:
            return None, None, "You're not linked to a campaign. Use `/join` first."

        from services.ai_dm import process_player_sms
        result = process_player_sms(text, char, campaign)
        return campaign, char, result

    with _flask_app.app_context():
        campaign, char, result = _do()

    if not campaign:
        await interaction.followup.send(result, ephemeral=True)
        return

    # Post result to the channel
    em = discord.Embed(
        description=f"**{char.name}**: _{text}_\n\n{result}",
        color=CLASS_COLORS.get(char.class_name, DM_COLOR),
    )
    await interaction.followup.send(embed=em)

    # Post to dice-log channel if there's a mechanical result
    if result.startswith('['):
        await _post_to_dice_log(campaign, char.name, result)

    # Bridge to SMS
    await _bridge_to_sms(campaign, char.name, text, result)


async def _post_to_dice_log(campaign, char_name, text):
    """Post a roll result to the dice-log channel."""
    state = campaign.current_state or {}
    channel_id = state.get('discord', {}).get('channels', {}).get('dice_log')
    if not channel_id:
        return
    channel = bot.get_channel(int(channel_id))
    if channel:
        em = roll_embed(char_name, text)
        await channel.send(embed=em)


async def _bridge_to_sms(campaign, char_name, player_msg, dm_response):
    """Forward Discord actions to SMS players."""
    state = campaign.current_state or {}
    if not state.get('sms_enabled'):
        return

    from models import User, Character
    with _flask_app.app_context():
        for player_id in (campaign.players or []):
            user = User.query.get(player_id)
            if not user or not user.phone_number:
                continue
            # Don't send to the acting player if they're also on SMS
            if user.discord_id:
                continue
            # Condense for SMS
            sms_text = f"[{char_name}] {player_msg}\nDM: {dm_response}"
            if len(sms_text) > 300:
                sms_text = sms_text[:297] + "..."
            from services.sms import send_sms
            send_sms(user.phone_number, sms_text)


# ── Channel setup ───────────────────────────────────────────

async def setup_campaign_channels(guild, campaign, dm_discord_user):
    """Create the channel category and game channels for a campaign."""
    # Create category
    category = await guild.create_category(f"🎲 {campaign.name}")

    # Quest board (read-only for players)
    quest_overwrites = {
        guild.default_role: discord.PermissionOverwrite(send_messages=False),
        guild.me: discord.PermissionOverwrite(send_messages=True),
    }
    quest_board = await guild.create_text_channel(
        "quest-board", category=category, overwrites=quest_overwrites,
        topic=f"Campaign overview for {campaign.name}"
    )

    # Main gameplay channels
    tavern = await guild.create_text_channel(
        "tavern", category=category,
        topic="Main gameplay — type /action to play!"
    )
    combat = await guild.create_text_channel(
        "combat", category=category,
        topic="Combat encounters and initiative tracking"
    )

    # Dice log (read-only)
    dice_overwrites = {
        guild.default_role: discord.PermissionOverwrite(send_messages=False),
        guild.me: discord.PermissionOverwrite(send_messages=True),
    }
    dice_log = await guild.create_text_channel(
        "dice-log", category=category, overwrites=dice_overwrites,
        topic="All dice rolls and mechanical results"
    )

    # Character sheets (read-only)
    char_overwrites = {
        guild.default_role: discord.PermissionOverwrite(send_messages=False),
        guild.me: discord.PermissionOverwrite(send_messages=True),
    }
    char_sheets = await guild.create_text_channel(
        "character-sheets", category=category, overwrites=char_overwrites,
        topic="Character information and stats"
    )

    # DM screen (DM only)
    dm_overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        dm_discord_user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
        guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True),
    }
    dm_screen = await guild.create_text_channel(
        "dm-screen", category=category, overwrites=dm_overwrites,
        topic="DM-only notes and controls"
    )

    # Debug channel (DM only — API activity, errors, diagnostics)
    debug_channel = await guild.create_text_channel(
        "debug", category=category, overwrites=dm_overwrites,
        topic="API activity log, errors, and diagnostics"
    )

    channels = {
        'category': str(category.id),
        'quest_board': str(quest_board.id),
        'tavern': str(tavern.id),
        'combat': str(combat.id),
        'dice_log': str(dice_log.id),
        'character_sheets': str(char_sheets.id),
        'dm_screen': str(dm_screen.id),
        'debug': str(debug_channel.id),
    }

    # Post welcome message to quest board
    welcome_em = discord.Embed(
        title=f"⚔ {campaign.name}",
        description=(
            f"Welcome to **{campaign.name}**!\n\n"
            f"**Join Code:** `{campaign.join_code}`\n\n"
            f"**How to play:**\n"
            f"1. Type `/join your_username` to link your account\n"
            f"2. Verify with `/verify {campaign.join_code}`\n"
            f"3. Head to #tavern and use `/action` to play!\n\n"
            f"**Quick commands:**\n"
            f"`/action I search the room` — Do something\n"
            f"`/roll 2d6+3` — Roll dice\n"
            f"`/attack goblin` — Attack an enemy\n"
            f"`/check perception` — Skill check\n"
            f"`/stats` — View your character sheet"
        ),
        color=DM_COLOR,
    )
    await quest_board.send(embed=welcome_em)

    # Post to DM screen
    dm_em = discord.Embed(
        title="🛡 DM Screen",
        description=(
            "This channel is only visible to you and the bot.\n\n"
            "**DM Commands:**\n"
            "`/scene <text>` — Set scene narration\n"
            "`/combat start` — Begin combat\n"
            "`/npc add <name> <hp> <ac>` — Add NPC\n"
            "`/npc say <name> <text>` — Speak as NPC\n"
            "`/damage @player <amount>` — Apply damage\n"
            "`/heal @player <amount>` — Heal a player\n"
            "`/whisper @player <text>` — Private message\n"
            "`/recap` — AI-generated session recap\n"
            "`/agent toggle @player` — Toggle AI autopilot"
        ),
        color=DM_COLOR,
    )
    await dm_screen.send(embed=dm_em)

    return channels


# ═══════════════════════════════════════════════════════════
# PLAYER COMMANDS
# ═══════════════════════════════════════════════════════════

@bot.tree.command(name="action", description="Describe what your character does")
@app_commands.describe(text="What do you do? e.g. 'I search the room for traps'")
async def action_cmd(interaction: discord.Interaction, text: str):
    await process_discord_action(interaction, text)


@bot.tree.command(name="roll", description="Roll dice (e.g. 2d6+3, d20, 4d8-1)")
@app_commands.describe(dice="Dice expression like 2d6+3")
async def roll_cmd(interaction: discord.Interaction, dice: str):
    def _do():
        campaign, char, user = _get_player_context(
            interaction.guild_id, interaction.user.id
        )
        char_name = char.name if char else interaction.user.display_name
        from services.engine import resolve_roll
        return resolve_roll(dice), char_name

    with _flask_app.app_context():
        result, char_name = _do()

    if result.get('error'):
        await interaction.response.send_message(f"❌ {result['error']}", ephemeral=True)
        return

    em = roll_embed(char_name, result['text'])
    await interaction.response.send_message(embed=em)


@bot.tree.command(name="attack", description="Attack a target")
@app_commands.describe(target="Who are you attacking?")
async def attack_cmd(interaction: discord.Interaction, target: str):
    await process_discord_action(interaction, f"I attack the {target}")


@bot.tree.command(name="check", description="Make a skill check")
@app_commands.describe(skill="Skill name (e.g. Perception, Stealth, Athletics)")
async def check_cmd(interaction: discord.Interaction, skill: str):
    await process_discord_action(interaction, f"I make a {skill} check")


@bot.tree.command(name="cast", description="Cast a spell")
@app_commands.describe(spell="Spell name", target="Target (optional)")
async def cast_cmd(interaction: discord.Interaction, spell: str, target: str = ""):
    text = f"I cast {spell}"
    if target:
        text += f" on {target}"
    await process_discord_action(interaction, text)


@bot.tree.command(name="save", description="Make a saving throw")
@app_commands.describe(ability="Ability: STR, DEX, CON, INT, WIS, or CHA")
async def save_cmd(interaction: discord.Interaction, ability: str):
    await process_discord_action(interaction, f"I make a {ability.upper()} saving throw")


@bot.tree.command(name="stats", description="View your character sheet")
async def stats_cmd(interaction: discord.Interaction):
    with _flask_app.app_context():
        campaign, char, user = _get_player_context(
            interaction.guild_id, interaction.user.id
        )
    if not char:
        await interaction.response.send_message(
            "You're not linked to a campaign. Use `/join` first.", ephemeral=True
        )
        return
    em = character_embed(char)
    await interaction.response.send_message(embed=em)


@bot.tree.command(name="inventory", description="View your equipment")
async def inventory_cmd(interaction: discord.Interaction):
    with _flask_app.app_context():
        campaign, char, user = _get_player_context(
            interaction.guild_id, interaction.user.id
        )
    if not char:
        await interaction.response.send_message(
            "You're not linked to a campaign. Use `/join` first.", ephemeral=True
        )
        return
    equip = char.equipment or []
    spells_data = char.spells or {}
    gold = spells_data.get('gold', 0)
    items = "\n".join(f"• {item}" for item in equip) if equip else "Empty"
    em = discord.Embed(
        title=f"🎒 {char.name}'s Inventory",
        description=f"{items}\n\n💰 **Gold:** {gold}",
        color=CLASS_COLORS.get(char.class_name, 0x808080),
    )
    await interaction.response.send_message(embed=em)


# ── Join / Verify ──

@bot.tree.command(name="join", description="Link your Discord to your game account")
@app_commands.describe(username="Your QuesterLedger username")
async def join_cmd(interaction: discord.Interaction, username: str):
    with _flask_app.app_context():
        from models import User
        campaign = _get_campaign_for_guild(interaction.guild_id)
        if not campaign:
            await interaction.response.send_message(
                "No campaign is linked to this server. A DM needs to run `/setup` first.",
                ephemeral=True,
            )
            return

        user = User.query.filter_by(username=username).first()
        if not user:
            await interaction.response.send_message(
                f"No account found for `{username}`. Register at the web app first.",
                ephemeral=True,
            )
            return

        # Store pending verification
        from sqlalchemy.orm.attributes import flag_modified
        from models import db
        state = campaign.current_state or {}
        pending = state.get('discord_pending_verifications', {})
        pending[str(interaction.user.id)] = {
            'user_id': user.id,
            'username': username,
        }
        state['discord_pending_verifications'] = pending
        campaign.current_state = state
        flag_modified(campaign, 'current_state')
        db.session.commit()

    await interaction.response.send_message(
        f"Almost there! Now type `/verify CODE` with the campaign join code your DM gave you.",
        ephemeral=True,
    )


@bot.tree.command(name="verify", description="Verify your account with the campaign join code")
@app_commands.describe(code="The campaign join code from your DM")
async def verify_cmd(interaction: discord.Interaction, code: str):
    with _flask_app.app_context():
        from models import User, Character, db
        from sqlalchemy.orm.attributes import flag_modified

        campaign = _get_campaign_for_guild(interaction.guild_id)
        if not campaign:
            await interaction.response.send_message("No campaign linked.", ephemeral=True)
            return

        state = campaign.current_state or {}
        pending = state.get('discord_pending_verifications', {})
        discord_id_str = str(interaction.user.id)

        if discord_id_str not in pending:
            await interaction.response.send_message(
                "No pending join. Use `/join your_username` first.", ephemeral=True
            )
            return

        if code.upper().strip() != campaign.join_code.upper():
            await interaction.response.send_message(
                "❌ Wrong code. Try again with `/verify CODE`.", ephemeral=True
            )
            return

        # Link the Discord account
        user_id = pending[discord_id_str]['user_id']
        user = User.query.get(user_id)
        if not user:
            await interaction.response.send_message("User not found.", ephemeral=True)
            return

        user.discord_id = discord_id_str
        del pending[discord_id_str]
        state['discord_pending_verifications'] = pending
        campaign.current_state = state
        flag_modified(campaign, 'current_state')
        db.session.commit()

        # Get character
        char = Character.query.filter_by(user_id=user.id, campaign_id=campaign.id).first()
        if not char:
            char = Character.query.filter_by(user_id=user.id).first()

    if char:
        em = character_embed(char)
        await interaction.response.send_message(
            f"✅ Verified! You're playing as **{char.name}**. Head to #tavern and use `/action` to play!",
            embed=em,
        )
        # Post character sheet to character-sheets channel
        state = campaign.current_state or {}
        cs_channel_id = state.get('discord', {}).get('channels', {}).get('character_sheets')
        if cs_channel_id:
            cs_channel = bot.get_channel(int(cs_channel_id))
            if cs_channel:
                await cs_channel.send(
                    f"**{interaction.user.display_name}** joined as:",
                    embed=em,
                )
    else:
        await interaction.response.send_message(
            f"✅ Verified! You're linked to {campaign.name}. Create a character on the web app.",
        )


# ═══════════════════════════════════════════════════════════
# DM COMMANDS
# ═══════════════════════════════════════════════════════════

@bot.tree.command(name="setup", description="[DM] Set up this server for a campaign")
@app_commands.describe(join_code="The campaign's join code")
async def setup_cmd(interaction: discord.Interaction, join_code: str):
    await interaction.response.defer()

    with _flask_app.app_context():
        from models import Campaign, User, db
        from sqlalchemy.orm.attributes import flag_modified

        campaign = Campaign.query.filter_by(join_code=join_code.upper().strip()).first()
        if not campaign:
            await interaction.followup.send("❌ No campaign found with that join code.", ephemeral=True)
            return

        # Link DM's discord account
        dm = User.query.get(campaign.dm_id)
        if dm:
            dm.discord_id = str(interaction.user.id)

        # Create channels
        channels = await setup_campaign_channels(
            interaction.guild, campaign, interaction.user
        )

        # Store Discord config in campaign state
        state = campaign.current_state or {}
        state['discord'] = {
            'guild_id': str(interaction.guild_id),
            'channels': channels,
            'enabled': True,
        }
        campaign.current_state = state
        flag_modified(campaign, 'current_state')
        db.session.commit()

    await interaction.followup.send(
        f"✅ **{campaign.name}** is set up! Channels created. "
        f"Share the join code `{campaign.join_code}` with your players.\n\n"
        f"Players: type `/join your_username` then `/verify {campaign.join_code}` to link your account."
    )


@bot.tree.command(name="scene", description="[DM] Narrate a scene")
@app_commands.describe(text="Scene description")
async def scene_cmd(interaction: discord.Interaction, text: str):
    with _flask_app.app_context():
        is_dm, campaign = _is_dm(interaction.guild_id, interaction.user.id)
    if not is_dm:
        await interaction.response.send_message("Only the DM can use this.", ephemeral=True)
        return

    # Optionally run through AI cleanup
    em = narration_embed(text)
    await interaction.response.send_message(embed=em)

    # Also post to combat channel if in combat
    with _flask_app.app_context():
        state = campaign.current_state or {}
        combat_ch_id = state.get('discord', {}).get('channels', {}).get('combat')
        if state.get('combat_active') and combat_ch_id:
            ch = bot.get_channel(int(combat_ch_id))
            if ch:
                await ch.send(embed=em)

    # Bridge to SMS
    await _bridge_to_sms(campaign, "DM", text, "")


# ── NPC command group ──

npc_group = app_commands.Group(name="npc", description="NPC management (DM only)")


@npc_group.command(name="add", description="[DM] Add an NPC to combat")
@app_commands.describe(name="NPC name", hp="Hit points", ac="Armor class", initiative="Initiative roll (auto if omitted)")
async def npc_add_cmd(interaction: discord.Interaction, name: str, hp: int, ac: int, initiative: int = 0):
    with _flask_app.app_context():
        is_dm, campaign = _is_dm(interaction.guild_id, interaction.user.id)
        if not is_dm:
            await interaction.response.send_message("DM only.", ephemeral=True)
            return

        from models import db, DiceRoller
        from sqlalchemy.orm.attributes import flag_modified

        state = campaign.current_state or {}
        order = state.get('initiative_order', [])

        if initiative == 0:
            initiative, _, _ = DiceRoller.roll('1d20')

        order.append({
            'name': name,
            'initiative': initiative,
            'is_npc': True,
            'npc_hp': hp,
            'npc_hp_max': hp,
            'npc_ac': ac,
            'roll_detail': f'd20={initiative}',
        })
        order.sort(key=lambda x: x['initiative'], reverse=True)
        state['initiative_order'] = order
        campaign.current_state = state
        flag_modified(campaign, 'current_state')
        db.session.commit()

    em = discord.Embed(
        description=f"👹 **{name}** enters the fray! (HP: {hp}, AC: {ac}, Init: {initiative})",
        color=COMBAT_COLOR,
    )
    await interaction.response.send_message(embed=em)


@npc_group.command(name="say", description="[DM] Speak as an NPC")
@app_commands.describe(name="NPC name", text="What the NPC says")
async def npc_say_cmd(interaction: discord.Interaction, name: str, text: str):
    with _flask_app.app_context():
        is_dm, campaign = _is_dm(interaction.guild_id, interaction.user.id)
    if not is_dm:
        await interaction.response.send_message("DM only.", ephemeral=True)
        return

    em = discord.Embed(
        description=f'*"{text}"*',
        color=0x95A5A6,
    )
    em.set_author(name=f"🗣 {name}")
    await interaction.response.send_message(embed=em)


bot.tree.add_command(npc_group)


# ── Combat command group ──

combat_group = app_commands.Group(name="combat", description="Combat management (DM only)")


@combat_group.command(name="start", description="[DM] Start combat and roll initiative")
async def combat_start_cmd(interaction: discord.Interaction):
    await interaction.response.defer()

    with _flask_app.app_context():
        is_dm, campaign = _is_dm(interaction.guild_id, interaction.user.id)
        if not is_dm:
            await interaction.followup.send("DM only.", ephemeral=True)
            return

        from models import db, Character, DiceRoller
        from services.engine import ability_modifier
        from sqlalchemy.orm.attributes import flag_modified

        state = campaign.current_state or {}
        order = state.get('initiative_order', [])

        # Roll initiative for all players
        for player_id in (campaign.players or []):
            char = Character.query.filter_by(user_id=player_id, campaign_id=campaign.id).first()
            if not char:
                char = Character.query.filter_by(user_id=player_id).first()
            if not char:
                continue

            dex_mod = ability_modifier((char.ability_scores or {}).get('DEX', 10))
            init_roll, rolls, _ = DiceRoller.roll('1d20', modifier=dex_mod)

            # Don't add if already in order
            if any(e.get('char_id') == char.id for e in order):
                continue

            order.append({
                'name': char.name,
                'initiative': init_roll,
                'char_id': char.id,
                'is_npc': False,
                'roll_detail': f'd20({rolls[0]})+{dex_mod}={init_roll}',
            })

        order.sort(key=lambda x: x['initiative'], reverse=True)
        state['initiative_order'] = order
        state['combat_active'] = True
        state['turn_index'] = 0
        state['round'] = 1
        campaign.current_state = state
        flag_modified(campaign, 'current_state')
        db.session.commit()

    em = combat_embed(campaign)
    await interaction.followup.send("⚔ **Combat has begun!** Roll initiative!", embed=em)

    # Also post to combat channel
    with _flask_app.app_context():
        combat_ch_id = state.get('discord', {}).get('channels', {}).get('combat')
    if combat_ch_id:
        ch = bot.get_channel(int(combat_ch_id))
        if ch:
            await ch.send(embed=em)


@combat_group.command(name="next", description="[DM] Advance to the next turn")
async def combat_next_cmd(interaction: discord.Interaction):
    with _flask_app.app_context():
        is_dm, campaign = _is_dm(interaction.guild_id, interaction.user.id)
        if not is_dm:
            await interaction.response.send_message("DM only.", ephemeral=True)
            return

        from models import db
        from sqlalchemy.orm.attributes import flag_modified

        state = campaign.current_state or {}
        order = state.get('initiative_order', [])
        if not order:
            await interaction.response.send_message("No combat active.", ephemeral=True)
            return

        turn_idx = state.get('turn_index', 0) + 1
        if turn_idx >= len(order):
            turn_idx = 0
            state['round'] = state.get('round', 1) + 1

        state['turn_index'] = turn_idx
        campaign.current_state = state
        flag_modified(campaign, 'current_state')
        db.session.commit()

    em = combat_embed(campaign)
    await interaction.response.send_message(embed=em)


@combat_group.command(name="end", description="[DM] End combat")
async def combat_end_cmd(interaction: discord.Interaction):
    with _flask_app.app_context():
        is_dm, campaign = _is_dm(interaction.guild_id, interaction.user.id)
        if not is_dm:
            await interaction.response.send_message("DM only.", ephemeral=True)
            return

        from models import db
        from sqlalchemy.orm.attributes import flag_modified

        state = campaign.current_state or {}
        state['combat_active'] = False
        state['initiative_order'] = []
        state['turn_index'] = 0
        state['round'] = 1
        campaign.current_state = state
        flag_modified(campaign, 'current_state')
        db.session.commit()

    em = discord.Embed(
        description="🕊 **Combat has ended.** Sheathe your weapons.",
        color=SUCCESS_COLOR,
    )
    await interaction.response.send_message(embed=em)


bot.tree.add_command(combat_group)


# ── Condition command group ──

condition_group = app_commands.Group(name="condition", description="Manage conditions (DM only)")


@condition_group.command(name="add", description="[DM] Apply a condition to a combatant")
@app_commands.describe(target="Character or NPC name", condition="Condition name (e.g. Poisoned, Stunned)")
async def condition_add_cmd(interaction: discord.Interaction, target: str, condition: str):
    with _flask_app.app_context():
        is_dm, campaign = _is_dm(interaction.guild_id, interaction.user.id)
        if not is_dm:
            await interaction.response.send_message("DM only.", ephemeral=True)
            return

        from models import db
        from sqlalchemy.orm.attributes import flag_modified

        state = campaign.current_state or {}
        conditions_map = state.get('active_conditions', {})

        # Find target in initiative order
        order = state.get('initiative_order', [])
        target_key = None
        for i, entry in enumerate(order):
            if entry['name'].lower() == target.lower():
                if entry.get('is_npc'):
                    target_key = f"npc_{i}"
                else:
                    target_key = f"char_{entry.get('char_id', i)}"
                break

        if not target_key:
            await interaction.response.send_message(f"'{target}' not found in combat.", ephemeral=True)
            return

        conds = conditions_map.get(target_key, [])
        if condition not in conds:
            conds.append(condition)
        conditions_map[target_key] = conds
        state['active_conditions'] = conditions_map
        campaign.current_state = state
        flag_modified(campaign, 'current_state')
        db.session.commit()

    await interaction.response.send_message(
        f"⚡ **{target}** is now **{condition}**!"
    )


@condition_group.command(name="remove", description="[DM] Remove a condition from a combatant")
@app_commands.describe(target="Character or NPC name", condition="Condition to remove")
async def condition_remove_cmd(interaction: discord.Interaction, target: str, condition: str):
    with _flask_app.app_context():
        is_dm, campaign = _is_dm(interaction.guild_id, interaction.user.id)
        if not is_dm:
            await interaction.response.send_message("DM only.", ephemeral=True)
            return

        from models import db
        from sqlalchemy.orm.attributes import flag_modified

        state = campaign.current_state or {}
        conditions_map = state.get('active_conditions', {})

        order = state.get('initiative_order', [])
        target_key = None
        for i, entry in enumerate(order):
            if entry['name'].lower() == target.lower():
                target_key = f"npc_{i}" if entry.get('is_npc') else f"char_{entry.get('char_id', i)}"
                break

        if not target_key:
            await interaction.response.send_message(f"'{target}' not found.", ephemeral=True)
            return

        conds = conditions_map.get(target_key, [])
        if condition in conds:
            conds.remove(condition)
        conditions_map[target_key] = conds
        state['active_conditions'] = conditions_map
        campaign.current_state = state
        flag_modified(campaign, 'current_state')
        db.session.commit()

    await interaction.response.send_message(
        f"✅ **{condition}** removed from **{target}**."
    )


bot.tree.add_command(condition_group)


# ── Other DM commands ──

@bot.tree.command(name="damage", description="[DM] Apply damage to a player or NPC")
@app_commands.describe(target="Character or NPC name", amount="Damage amount")
async def damage_cmd(interaction: discord.Interaction, target: str, amount: int):
    with _flask_app.app_context():
        is_dm, campaign = _is_dm(interaction.guild_id, interaction.user.id)
        if not is_dm:
            await interaction.response.send_message("DM only.", ephemeral=True)
            return

        from models import db, Character
        from sqlalchemy.orm.attributes import flag_modified

        # Check NPCs first
        state = campaign.current_state or {}
        order = state.get('initiative_order', [])
        for entry in order:
            if entry.get('is_npc') and entry['name'].lower() == target.lower():
                old_hp = entry.get('npc_hp', 0)
                entry['npc_hp'] = max(0, old_hp - amount)
                campaign.current_state = state
                flag_modified(campaign, 'current_state')
                db.session.commit()
                defeated = " **DEFEATED!**" if entry['npc_hp'] == 0 else ""
                await interaction.response.send_message(
                    f"💥 **{entry['name']}** takes {amount} damage! "
                    f"(HP: {entry['npc_hp']}/{entry['npc_hp_max']}){defeated}"
                )
                return

        # Check PCs
        char = Character.query.filter(
            Character.name.ilike(target),
            Character.campaign_id == campaign.id
        ).first()
        if not char:
            char = Character.query.filter(Character.name.ilike(target)).first()
        if char:
            char.hp_current = max(0, char.hp_current - amount)
            db.session.commit()
            await interaction.response.send_message(
                f"💥 **{char.name}** takes {amount} damage! "
                f"(HP: {char.hp_current}/{char.hp_max})"
            )
            return

    await interaction.response.send_message(f"'{target}' not found.", ephemeral=True)


@bot.tree.command(name="heal", description="[DM] Heal a player or NPC")
@app_commands.describe(target="Character or NPC name", amount="Healing amount")
async def heal_cmd(interaction: discord.Interaction, target: str, amount: int):
    with _flask_app.app_context():
        is_dm, campaign = _is_dm(interaction.guild_id, interaction.user.id)
        if not is_dm:
            await interaction.response.send_message("DM only.", ephemeral=True)
            return

        from models import db, Character
        from sqlalchemy.orm.attributes import flag_modified

        # Check NPCs
        state = campaign.current_state or {}
        order = state.get('initiative_order', [])
        for entry in order:
            if entry.get('is_npc') and entry['name'].lower() == target.lower():
                entry['npc_hp'] = min(entry['npc_hp_max'], entry.get('npc_hp', 0) + amount)
                campaign.current_state = state
                flag_modified(campaign, 'current_state')
                db.session.commit()
                await interaction.response.send_message(
                    f"💚 **{entry['name']}** healed for {amount}! "
                    f"(HP: {entry['npc_hp']}/{entry['npc_hp_max']})"
                )
                return

        # Check PCs
        char = Character.query.filter(
            Character.name.ilike(target),
            Character.campaign_id == campaign.id
        ).first()
        if not char:
            char = Character.query.filter(Character.name.ilike(target)).first()
        if char:
            char.hp_current = min(char.hp_max, char.hp_current + amount)
            db.session.commit()
            await interaction.response.send_message(
                f"💚 **{char.name}** healed for {amount}! "
                f"(HP: {char.hp_current}/{char.hp_max})"
            )
            return

    await interaction.response.send_message(f"'{target}' not found.", ephemeral=True)


@bot.tree.command(name="loot", description="[DM] Give an item to a player")
@app_commands.describe(target="Character name", item="Item to give")
async def loot_cmd(interaction: discord.Interaction, target: str, item: str):
    with _flask_app.app_context():
        is_dm, campaign = _is_dm(interaction.guild_id, interaction.user.id)
        if not is_dm:
            await interaction.response.send_message("DM only.", ephemeral=True)
            return

        from models import db, Character
        from sqlalchemy.orm.attributes import flag_modified

        char = Character.query.filter(
            Character.name.ilike(target),
            Character.campaign_id == campaign.id
        ).first()
        if not char:
            char = Character.query.filter(Character.name.ilike(target)).first()
        if not char:
            await interaction.response.send_message(f"'{target}' not found.", ephemeral=True)
            return

        equip = char.equipment or []
        equip.append(item)
        char.equipment = equip
        flag_modified(char, 'equipment')
        db.session.commit()

    em = discord.Embed(
        description=f"🎁 **{char.name}** received **{item}**!",
        color=DM_COLOR,
    )
    await interaction.response.send_message(embed=em)


@bot.tree.command(name="whisper", description="[DM] Send a private message to a player")
@app_commands.describe(player="The Discord user", text="Secret message")
async def whisper_cmd(interaction: discord.Interaction, player: discord.Member, text: str):
    with _flask_app.app_context():
        is_dm, campaign = _is_dm(interaction.guild_id, interaction.user.id)
    if not is_dm:
        await interaction.response.send_message("DM only.", ephemeral=True)
        return

    # Create a private thread
    try:
        thread = await interaction.channel.create_thread(
            name=f"DM whisper to {player.display_name}",
            type=discord.ChannelType.private_thread,
        )
        em = discord.Embed(
            description=f"🤫 *The DM whispers:*\n\n{text}",
            color=DM_COLOR,
        )
        await thread.send(f"{player.mention}", embed=em)
        await interaction.response.send_message(
            f"Whisper sent to {player.display_name} in a private thread.", ephemeral=True
        )
    except discord.Forbidden:
        await interaction.response.send_message(
            "Can't create private threads. Check bot permissions.", ephemeral=True
        )


@bot.tree.command(name="recap", description="[DM] Generate an AI recap of the session")
async def recap_cmd(interaction: discord.Interaction):
    await interaction.response.defer()

    with _flask_app.app_context():
        is_dm, campaign = _is_dm(interaction.guild_id, interaction.user.id)
        if not is_dm:
            await interaction.followup.send("DM only.", ephemeral=True)
            return

        from services.engine import get_recent_log, get_combat_state_summary
        from services.ai_dm import _call

        recent = get_recent_log(campaign, count=20)
        combat = get_combat_state_summary(campaign)

        messages = [
            {
                "role": "system",
                "content": (
                    "You are a D&D session recap writer. Write a dramatic, concise recap "
                    "of recent events. Use past tense. Under 500 characters. "
                    "Focus on key moments, dramatic turns, and player achievements."
                ),
            },
            {
                "role": "user",
                "content": f"Campaign: {campaign.name}\nGame state: {combat}\n\nRecent events:\n{recent}\n\nWrite the recap.",
            },
        ]

        text, error = _call(messages, temperature=0.8, max_tokens=250)
        if error:
            text = f"*No recap available: {error}*"

    em = discord.Embed(
        title=f"📜 Session Recap — {campaign.name}",
        description=text,
        color=DM_COLOR,
    )
    await interaction.followup.send(embed=em)


@bot.tree.command(name="agent", description="[DM] Toggle AI agent mode for a player")
@app_commands.describe(player="The Discord user to toggle agent mode for")
async def agent_cmd(interaction: discord.Interaction, player: discord.Member):
    with _flask_app.app_context():
        is_dm, campaign = _is_dm(interaction.guild_id, interaction.user.id)
        if not is_dm:
            await interaction.response.send_message("DM only.", ephemeral=True)
            return

        from models import User, db
        from sqlalchemy.orm.attributes import flag_modified

        user = User.query.filter_by(discord_id=str(player.id)).first()
        if not user:
            await interaction.response.send_message(
                f"{player.display_name} hasn't linked their account.", ephemeral=True
            )
            return

        state = campaign.current_state or {}
        agent_players = state.get('agent_mode_players', [])

        if user.id in agent_players:
            agent_players.remove(user.id)
            status = "disabled"
        else:
            agent_players.append(user.id)
            status = "enabled"

        state['agent_mode_players'] = agent_players
        campaign.current_state = state
        flag_modified(campaign, 'current_state')
        db.session.commit()

    emoji = "🤖" if status == "enabled" else "👤"
    await interaction.response.send_message(
        f"{emoji} AI Agent mode **{status}** for **{player.display_name}**."
    )


# ═══════════════════════════════════════════════════════════
# SMS → DISCORD BRIDGE (called from Flask thread)
# ═══════════════════════════════════════════════════════════

def post_to_discord(campaign, char_name, player_msg, dm_response, source="sms"):
    """Post an SMS action to the Discord tavern channel. Thread-safe."""
    if _bot_loop is None or bot.is_closed():
        return

    state = campaign.current_state or {}
    discord_cfg = state.get('discord', {})
    if not discord_cfg.get('enabled'):
        return

    tavern_id = discord_cfg.get('channels', {}).get('tavern')
    if not tavern_id:
        return

    async def _post():
        channel = bot.get_channel(int(tavern_id))
        if not channel:
            return

        icon = "📱" if source == "sms" else "🤖"
        em = discord.Embed(
            description=(
                f"{icon} **{char_name}** *(via {source.upper()})*: _{player_msg}_\n\n"
                f"{dm_response}"
            ),
            color=DM_COLOR,
        )
        await channel.send(embed=em)

    asyncio.run_coroutine_threadsafe(_post(), _bot_loop)


# ═══════════════════════════════════════════════════════════
# BOT LIFECYCLE
# ═══════════════════════════════════════════════════════════

def invite_url():
    """Generate the bot invite URL."""
    client_id = os.environ.get('DISCORD_CLIENT_ID', '')
    if not client_id and bot.user:
        client_id = str(bot.user.id)
    if not client_id:
        return "Bot not connected — set DISCORD_CLIENT_ID"

    permissions = discord.Permissions(
        manage_channels=True,
        send_messages=True,
        send_messages_in_threads=True,
        create_private_threads=True,
        embed_links=True,
        read_message_history=True,
        add_reactions=True,
        manage_messages=True,
        manage_roles=True,
    )
    return discord.utils.oauth_url(
        client_id, permissions=permissions,
        scopes=["bot", "applications.commands"],
    )


def run_bot(flask_app, token):
    """Start the bot in a new event loop (called from a background thread)."""
    import sys
    global _flask_app, _bot_loop
    _flask_app = flask_app
    loop = asyncio.new_event_loop()
    _bot_loop = loop
    asyncio.set_event_loop(loop)
    try:
        print(f'[Discord] Connecting with token {token[:20]}...', flush=True)
        loop.run_until_complete(bot.start(token))
    except Exception as e:
        print(f'[Discord] Bot error: {e}', file=sys.stderr, flush=True)
        import traceback
        traceback.print_exc()


def start_discord_bot(flask_app):
    """Start the Discord bot in a daemon thread. Call from app startup."""
    token = os.environ.get('DISCORD_BOT_TOKEN', '')
    if not token:
        print('[Discord] DISCORD_BOT_TOKEN not set — bot disabled.')
        return
    print('[Discord] Starting bot...')
    thread = threading.Thread(target=run_bot, args=(flask_app, token), daemon=True)
    thread.start()
