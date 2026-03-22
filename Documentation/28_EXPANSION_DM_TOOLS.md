# Expansion DM Tools Reference

DM-facing content from Xanathar's Guide to Everything (XGtE) and Tasha's Cauldron of Everything (TCoE). Covers group patrons, sidekicks, puzzles, traps, downtime, tool proficiency expansion, and supernatural environments.

---

## Group Patrons (TCoE)

A group patron is an NPC or organization that sponsors the adventuring party. Gives the DM a built-in quest hook system and the party a reason to work together.

### Patron Types

**Academy**: School, university, or research institution. Party members are students, faculty, or field researchers. Quest hooks: retrieve lost texts, investigate phenomena, protect researchers, compete with rival institutions. Perks: access to libraries, labs, identification services, research assistants.

**Ancient Being**: Dragon, archfey, celestial, fiend, or other powerful entity. Party works as agents or servants. Quest hooks: collect components, eliminate rivals, investigate threats to the patron, recover artifacts. Perks: supernatural gifts, divination, plane-hopping, access to the being's knowledge. Risk: the patron has its own agenda and may not be trustworthy.

**Aristocrat**: Noble family, royal court, merchant prince. Party serves as agents, bodyguards, or problem solvers. Quest hooks: political intrigue, trade route protection, rival nobles, succession crises. Perks: wealth, social connections, legal immunity, access to noble estates.

**Criminal Syndicate**: Thieves' guild, smuggling ring, crime family. Quest hooks: heists, turf wars, law enforcement evasion, protection rackets. Perks: fences for stolen goods, safe houses, forged documents, information networks. Risk: law enforcement attention.

**Guild**: Artisan guild, merchant guild, adventurer's guild. Quest hooks: protect trade routes, investigate counterfeit goods, reclaim resources, guild politics. Perks: crafting discounts, guild contacts, warehouse access.

**Military Force**: Army, militia, navy, or special forces. Quest hooks: reconnaissance, sabotage, escort missions, monster elimination, battlefield missions. Perks: equipment, training, military intelligence, rank advancement.

**Religious Order**: Temple, monastery, paladin order, or cult. Quest hooks: protect sacred sites, recover relics, combat undead/fiends, investigate heresies. Perks: healing, divination, blessings, sanctuary.

**Sovereign**: King, queen, emperor, or elected leader. Party serves as agents of the crown. Quest hooks: diplomacy, espionage, monster hunting, border conflicts, political threats. Perks: authority, resources, intelligence, royal decree backing.

### Using Patrons with an LLM
When running a campaign: assign a patron type early. Generate quests that align with the patron's interests. Escalate tension by putting the patron in conflict with the party's personal goals. The patron should have their own agenda that sometimes aligns and sometimes conflicts with the party.

---

## Sidekick Rules (TCoE)

Sidekicks are simplified NPC companions that can level up alongside the party. Built from any creature stat block of CR 1/2 or lower.

### Sidekick Classes

**Expert**: Skill-focused sidekick.
- Hit Die: d8
- Proficiencies: Light armor, simple weapons, two tools, three skills
- Key Features:
  - Helpful (Level 1): Help action as bonus action
  - Expertise (Level 3, 9): Double PB on two skill checks
  - Reliable Talent (Level 11): Minimum roll of 10 on proficient ability checks
  - Extra Attack (Level 6)
- Good for: Scout, face, skill monkey companion

**Spellcaster**: Choose Healer (WIS), Mage (INT), or Prodigy (CHA).
- Hit Die: d8
- Spellcasting: Full progression (cantrips + spell slots 1st-5th level by 17th)
- Spell list based on role:
  - Healer: Cure Wounds, Lesser Restoration, Revivify, Heal, etc.
  - Mage: Mage Hand, Fireball, Counterspell, Wall of Force, etc.
  - Prodigy: Light, Charm Person, Suggestion, Compulsion, etc.
- Key Features:
  - Potent Cantrips (Level 6): Add ability mod to cantrip damage
  - Empowered Spells (Level 14): Add ability mod to spell damage once per turn
- Good for: Healing support, ranged damage, or social/charm support

**Warrior**: Combat-focused sidekick.
- Hit Die: d10
- Proficiencies: All armor, shields, simple and martial weapons
- Key Features:
  - Martial Role (Level 1): Choose Attacker (+2 damage) or Defender (use reaction to impose disadvantage on attack against ally within 5 ft)
  - Extra Attack (Level 6)
  - Improved Critical (Level 15): Crit on 19-20
  - Second Wind (Level 1), Improved Defense (Level 10), Battle Readiness (Level 18)
- Good for: Tank, melee damage dealer, bodyguard

### Sidekick Notes for LLM
- Sidekicks should be simpler than PCs — fewer options, straightforward combat
- They don't get ASIs/feats unless the DM grants them
- Level up when the party does
- Use the base creature's stats as the starting point — just add class features on top

---

## Puzzles (TCoE)

TCoE provides 14 ready-to-use puzzles. Categories:

### Puzzle Design Principles
- Difficulty: Easy (DC 10-12), Medium (DC 13-15), Hard (DC 16-20)
- Always provide at least 3 paths to solve (logic, brute force, magic)
- Let Investigation, Arcana, Insight, Perception checks provide hints — not solutions
- If the party is truly stuck, offer a hint per Intelligence check (DC 15)
- Time pressure increases tension — add a countdown or consequences for failure

### Example Puzzles (Abbreviated)

**All That Glitters** (Difficulty: Easy)
- Room with gems embedded in walls. Each gem glows a different color.
- Solution requires placing gems in a specific pattern based on a riddle
- Skill hints: Arcana DC 12 identifies magical resonance, Investigation DC 12 notices pattern

**Exact Change** (Difficulty: Medium)
- Lock requiring a specific combination derived from coin weights/values
- Mathematical puzzle — players must calculate the right combination
- Skill hints: Investigation DC 15, History DC 13

**Eye of the Beholder** (Difficulty: Hard)
- Paintings that respond to being viewed in the correct order
- Solution involves interpreting artistic symbolism and arranging viewing sequence
- Skill hints: Perception DC 15, Insight DC 17

**Members Only** (Difficulty: Medium)
- Door that opens only for "members" — party must figure out the membership criteria
- Social deduction puzzle — clues hidden in the environment
- Skill hints: Investigation DC 14, Persuasion DC 15

### LLM Puzzle Usage
When generating puzzles: provide the setup, 3 clues, the solution, and what happens on failure. Scale difficulty to party level. Allow creative solutions — if the party's approach is clever and makes sense, let it work.

---

## Traps Revisited (XGtE)

XGtE expanded trap design with two categories: simple traps and complex traps.

### Simple Traps
One-time triggers. Detect with Investigation or Perception vs. trap DC. Disarm with thieves' tools vs. trap DC.

| Severity | Save DC | Attack Bonus | Damage (1-4) | Damage (5-10) | Damage (11-16) | Damage (17-20) |
|---|---|---|---|---|---|---|
| Setback | 10-11 | +3 to +5 | 1d10 | 2d10 | 4d10 | 10d10 |
| Dangerous | 12-15 | +6 to +8 | 2d10 | 4d10 | 10d10 | 18d10 |
| Deadly | 16-20 | +9 to +12 | 4d10 | 10d10 | 18d10 | 24d10 |

### Complex Traps
Multi-round threats that act on initiative. They have:
- **Active Elements**: What the trap does each round (attacks, environmental changes)
- **Dynamic Elements**: How the trap changes or escalates over time
- **Constant Elements**: Ongoing effects (difficult terrain, darkness, etc.)
- **Countermeasures**: How to disable, avoid, or survive

Complex traps have an initiative count (usually 20 and sometimes 10). They make attacks or force saves each round. Disabling requires multiple ability checks targeting different components.

### Example Complex Traps

**Sphere of Crushing Doom**: Walls close in over 4 rounds. Round 1: room shrinks 10 ft. Round 2: 20 ft. Round 3: creatures take 5d10 bludgeoning. Round 4: 10d10 and trapped. Countermeasure: STR DC 20 to hold walls (delays 1 round), thieves' tools DC 20 to disable mechanism (2 successes needed).

**Path of Blades**: 10-ft wide corridor with spinning blades. Initiative 20: each creature in corridor, +8 attack, 2d10 slashing. Initiative 10: blades reverse direction, +8 again. Countermeasure: DEX (Acrobatics) DC 15 to tumble through, Athletics DC 15 to barrel past, thieves' tools DC 15 (each success disables one blade — 3 needed for full disable).

---

## Downtime Activities (XGtE)

Expanded downtime activities beyond the PHB basics.

### Buying a Magic Item
- Time: 1 workweek minimum
- Expenses: 100 gp minimum (bribes, finder's fees)
- Resolution: Make a Persuasion + Investigation check. Total determines what's available:
  - 10-19: 1d6 Common items
  - 20-29: 1d6 Common + 1d4 Uncommon
  - 30-39: 1d6 Common + 1d4 Uncommon + 1 Rare
  - 40+: 1d6 Common + 1d4 Uncommon + 1 Rare + 1 Very Rare
- Complication chance: 10% per week spent searching

### Crafting a Magic Item
- Requires: formula (recipe), exotic materials, tool proficiency, spell if item replicates one
- Time and cost by rarity:

| Rarity | Workweeks | Cost |
|---|---|---|
| Common | 1 | 50 gp |
| Uncommon | 2 | 200 gp |
| Rare | 10 | 2,000 gp |
| Very Rare | 25 | 20,000 gp |
| Legendary | 50 | 100,000 gp |

- Requires a spellcaster if the item casts a spell. That caster must provide the spell each day of crafting.
- Multiple characters can contribute — divide time by number of crafters.

### Carousing
- 1 workweek, cost varies by lifestyle (10-250 gp)
- Make a Persuasion check:
  - 1-5: hostile contact (enemy, jilted NPC, gambling debt)
  - 6-10: nothing notable
  - 11-15: ally contact (friendly NPC, information source)
  - 16-20: ally contact + they owe you a favor
  - 21+: ally contact + significant favor + you gain a reputation

### Crime
- 1 workweek preparation + execution
- Make three checks: Stealth, thieves' tools, one of (Deception, Persuasion, Intimidation)
  - 0 successes: caught, face consequences
  - 1 success: partial haul (half value), possible heat
  - 2 successes: full haul
  - 3 successes: full haul + bonus (extra loot or useful information)
- Payout: 50 gp (petty crime) to 1,000+ gp (major heist). DM determines.

### Gambling
- 1 workweek, stake varies
- Make three checks from: Insight, Deception, Intimidation
  - 0 successes: lose stake + owe that much again
  - 1 success: lose half the stake
  - 2 successes: win 1.5× stake
  - 3 successes: win 2× stake
- 10% complication chance (cheating accusation, rival gambler grudge, etc.)

### Pit Fighting
- 1 workweek
- Make three checks: Athletics, Acrobatics, one special (DM's choice — Insight, Intimidation, Medicine)
  - 0 successes: lose, 3d6 bludgeoning damage
  - 1 success: lose narrowly, 2d6 bludgeoning
  - 2 successes: win (100 gp purse)
  - 3 successes: win big (200 gp purse, gain a reputation)

### Research
- 1 workweek, 50 gp expenses
- Intelligence check (+ appropriate proficiency if relevant)
- DM reveals one piece of lore per 50 gp spent, with accuracy/detail based on the check result
- Research can answer specific questions about monsters, locations, magic items, NPCs, or history

### Scribing a Spell Scroll
Time and cost by spell level:

| Level | Time | Cost |
|---|---|---|
| Cantrip | 1 day | 15 gp |
| 1st | 1 day | 25 gp |
| 2nd | 3 days | 250 gp |
| 3rd | 1 workweek | 500 gp |
| 4th | 2 workweeks | 2,500 gp |
| 5th | 4 workweeks | 5,000 gp |
| 6th | 8 workweeks | 15,000 gp |
| 7th | 16 workweeks | 25,000 gp |
| 8th | 32 workweeks | 50,000 gp |
| 9th | 48 workweeks | 250,000 gp |

Must be a spell you know/have prepared. Must provide material components (consumed).

### Training
- 10 workweeks, 25 gp/workweek
- Gain proficiency in one language or tool
- Must find a trainer

---

## Tool Proficiency Expansion (XGtE)

XGtE gave every tool proficiency actual mechanical uses. Key ones:

### Artisan's Tools

**Alchemist's Supplies**: Identify substance (Arcana), start fire (DEX DC 15), neutralize acid (Sleight of Hand). Can craft acid, alchemist's fire, antitoxin, oil, perfume, soap.

**Brewer's Supplies**: Identify drink (INT), detect poison in drink (Perception advantage), purify water (1 gallon/hour).

**Cook's Utensils**: Prepare a meal for up to 6 people per long rest. Everyone who eats it regains 1 extra HP per Hit Die spent during short rests for the next 24 hours.

**Herbalism Kit**: Identify plants (Nature advantage), make antitoxin (1 day, 25 gp), make healing potion (1 day, 25 gp).

**Poisoner's Kit**: Handle poison without risk of self-poisoning. Identify poisons (INT advantage). Apply poison to a weapon (1 minute).

**Smith's Tools**: Repair metal objects (1 hour, repair 10 HP to the object). Identify metal (History/Investigation advantage).

**Thieves' Tools**: Disarm traps, pick locks (DEX check vs. DC). Advantage on Investigation to find traps. Can set traps (DC depends on materials and time).

**Tinker's Tools**: Repair devices, jury-rig temporary fixes (1d4 hours), improve or build mechanisms.

### Other Tool Proficiencies

**Disguise Kit**: Create a disguise (1-10 minutes). Advantage on Deception to maintain it.

**Forgery Kit**: Create forged documents (1d4 hours for simple, 2d4 for complex). Advantage on Deception checks involving the forgery.

**Navigator's Tools**: Determine cardinal direction, plot course at sea, estimate arrival time. Advantage on Survival to avoid getting lost at sea.

**Gaming Sets**: Win or lose at gambling (Insight/Deception advantages during games). Gain information from opponents during play.

**Musical Instruments**: Advantage on Performance checks with the instrument. Can earn modest lifestyle during downtime.

**Vehicles**: Operate the vehicle type (land or water). Advantage on checks to maintain/repair. Navigate terrain.

### Tool + Skill Synergy
XGtE's key design: when you have both a relevant tool proficiency AND a relevant skill proficiency, you get advantage on the ability check. Examples:
- Investigation + Thieves' Tools: advantage when searching for traps
- Persuasion + Brewer's Supplies: advantage when plying someone with drinks
- Arcana + Alchemist's Supplies: advantage when identifying a potion
- Medicine + Herbalism Kit: advantage when treating diseases with herbs

---

## Supernatural Environments (TCoE)

TCoE introduced rules for regions warped by magical influence. These create ongoing environmental effects.

### Supernatural Region Types

**Blessed Radiance**: Celestial influence. Effects: healing spells gain bonus HP equal to spell level, undead have disadvantage on saves, short rests heal extra 1d6, flowers bloom, creatures feel calm.

**Far Realm**: Aberrant influence. Effects: creatures hear whispers (WIS DC 12 or frightened), Perception checks have disadvantage, plants twist unnaturally, compasses spin, short rests trigger nightmares (WIS DC 10 or no benefit).

**Haunted**: Ghost/undead influence. Effects: Perception checks to hear have disadvantage (constant whispers), candles and fires dim to half range, shadows move independently, dead bodies animate after 24 hours (DM decides as what).

**Infested**: Ooze/fungal influence. Effects: surfaces are slippery (DEX DC 12 or fall prone when moving more than half speed), metal corrodes (nonmagical metal weapons/armor lose 1 AC or attack/damage after 24 hours), air is toxic (CON DC 10 or poisoned for 1 hour after first breathing).

**Mirror Zone**: Feywild influence. Effects: reflections move independently, mirrors become portals (DM determines), duplicates of party members appear and mimic actions, gravity reverses in pockets.

**Psychic Resonance**: Psionic influence. Effects: telepathy range doubles, concentration checks have disadvantage, emotions amplify (advantage on CHA checks, disadvantage on WIS saves), objects levitate randomly.

**Unraveling Magic**: Wild magic zone. Effects: casting a spell triggers a DC 10 + spell level ability check or roll on Wild Magic Surge table. Completed spells sometimes produce additional unintended effects. Magic items occasionally suppress for 1d4 rounds.

### Using Supernatural Environments
Layer 1-3 effects from a region type onto a dungeon or wilderness area. Pick effects that challenge the party's strengths. Telegraphing effects works better than springing them — let the party see evidence of the zone before entering.

---

## Session Zero Guidance (TCoE)

TCoE provides a Session Zero framework. Key topics to address:

### Group Expectations
- Campaign tone (heroic, gritty, horror, comedy)
- Content boundaries (gore, romance, specific phobias)
- PvP policy
- Character death frequency
- Treasure and magic item expectations

### Party Composition
- Role coverage (healer, tank, utility, damage)
- Backstory connections between characters
- Shared goals or conflicting goals (both can work, but discuss)
- Power level expectations (optimized vs. thematic)

### Table Rules
- Attendance expectations
- Phone/distraction policy
- Rules disputes (DM decides vs. look it up)
- Retcon policy
- Homebrew allowances

For LLM use: when starting a campaign, run through these topics with the player(s) to establish expectations before play begins.
