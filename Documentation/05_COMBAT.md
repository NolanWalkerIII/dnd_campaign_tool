# Combat Rules

## Combat Flow

1. **Determine surprise** — If one side is unaware, they're surprised (can't move or take actions on first turn, no reactions until first turn ends).
2. **Establish positions** — Place combatants on the map (or describe positions in theater of the mind).
3. **Roll initiative** — Everyone rolls d20 + DEX modifier. Highest goes first. Ties: DM decides (common approach: higher DEX mod goes first, or players before monsters).
4. **Take turns** — Each creature gets one turn per round. A round represents ~6 seconds of in-game time.
5. **Repeat** until combat ends.

## Your Turn

On your turn you get:
- **1 Action**
- **1 Bonus Action** (only if you have a feature/spell that uses one)
- **Movement** (up to your speed)
- **1 free object interaction** (draw a weapon, open a door, pick up an item)

You also have **1 Reaction** per round (not per turn). Resets at the start of your turn.

Movement, action, and bonus action can be interleaved in any order. You can move, attack, move again (splitting movement).

---

## Actions in Combat

### Attack
Make one melee or ranged attack (or more with Extra Attack).

**Melee attack**: d20 + STR mod + proficiency (if proficient). Finesse weapons can use DEX instead.

**Ranged attack**: d20 + DEX mod + proficiency (if proficient). Thrown weapons can use STR.

**Damage**: Roll weapon's damage die + ability modifier.

### Cast a Spell
Cast a spell with a casting time of 1 action. See `06_SPELLCASTING.md`.

### Dash
Double your movement for the turn. You don't literally move — you gain additional movement equal to your speed.

### Disengage
Your movement doesn't provoke opportunity attacks for the rest of the turn.

### Dodge
Until the start of your next turn: attack rolls against you have disadvantage (if you can see the attacker), and you make DEX saves with advantage. Lost if incapacitated or speed drops to 0.

### Help
Give one ally advantage on their next ability check for a specific task, OR give them advantage on their next attack roll against a creature within 5 ft of you. The advantage only applies to the next relevant roll before the start of your next turn.

### Hide
Make a DEX (Stealth) check. If you succeed (contested by Perception), you're hidden — unseen and unheard. You gain advantage on your next attack roll. Attacking or being revealed breaks hiding.

### Ready
Prepare an action to trigger later. Specify a perceivable trigger and the action you'll take. When the trigger occurs, use your reaction to take the action. If readying a spell: you cast it on your turn (spending the slot and concentration) but hold it with your reaction to release when triggered. If you don't release it, the spell and slot are wasted.

### Search
Make a WIS (Perception) or INT (Investigation) check to find something.

### Use an Object
Interact with a second object (first one is your free interaction), or use an item that requires an action (healer's kit, potion, etc.).

---

## Bonus Actions

You only get a bonus action if something specifically grants one. Common sources:
- **Two-weapon fighting**: Attack with off-hand light weapon (no ability mod to damage unless you have the Fighting Style)
- **Rogue Cunning Action**: Dash, Disengage, or Hide
- **Monk Ki features**: Flurry of Blows, Patient Defense, Step of the Wind
- **Barbarian Rage**: Activate rage
- **Spells with bonus action casting time**: Healing Word, Misty Step, Shield of Faith, Hex, Hunter's Mark, Spiritual Weapon
- **Fighter Second Wind**: Regain HP
- **Paladin / Cleric Channel Divinity** (some options)

**Important rule**: If you cast a spell as a bonus action, the only other spell you can cast that turn is a cantrip with a casting time of 1 action. This catches people off guard — you can't Healing Word + Fireball in the same turn.

---

## Reactions

One per round. Resets at the start of your turn. Common reactions:

- **Opportunity Attack**: When a hostile creature you can see moves out of your reach, you can use your reaction to make one melee attack against it. Doesn't trigger if they Disengage, are moved involuntarily (shoved, Thunderwave), or teleport.
- **Shield** (spell): +5 AC until start of next turn. Reaction when hit.
- **Counterspell**: When you see a creature casting a spell within 60 ft. Automatically counters spells of 3rd level or lower (or the slot used). Higher level: ability check DC = 10 + spell level.
- **Absorb Elements**: When you take acid, cold, fire, lightning, or thunder damage.
- **Hellish Rebuke**: When you take damage.
- **Uncanny Dodge** (Rogue): Halve damage from an attack you can see.

---

## Attack Rolls

### Melee Attacks
- Normal reach: 5 ft
- Reach weapons (glaive, halberd, pike, whip): 10 ft
- Unarmed strikes: always available, 1 + STR mod bludgeoning damage (unless improved by class features)

### Ranged Attacks
- Each ranged weapon has a normal range and long range
- Attacking at long range: disadvantage
- Attacking beyond long range: impossible
- **Ranged attacks in melee**: If a hostile creature is within 5 ft and can see you, you have disadvantage on ranged attack rolls. Applies to ranged spell attacks too.

### Critical Hits
Natural 20 on the attack roll. Roll all damage dice twice (including Sneak Attack, Smite, etc.), then add modifiers once. Some features expand crit range (Champion Fighter crits on 19-20 at level 3, 18-20 at level 15).

### Critical Misses
Natural 1 always misses. No additional penalties RAW (no fumble tables by default — that's a houserule).

---

## Damage and Healing

### Damage Types
Bludgeoning, Piercing, Slashing, Acid, Cold, Fire, Force, Lightning, Necrotic, Poison, Psychic, Radiant, Thunder.

### Resistance and Vulnerability
- **Resistance**: Take half damage of that type (rounded down).
- **Vulnerability**: Take double damage.
- Multiple sources of resistance don't stack. Same with vulnerability.
- If a creature has both resistance and vulnerability to the same type, they cancel.

### Healing
Regain HP from spells, potions, class features, Hit Dice during short rests. HP can't exceed maximum.

### Temporary Hit Points
- Don't stack — take the higher value if you'd gain more
- Disappear after a long rest (or when specified)
- Removed before real HP
- Not actual hit points — healing doesn't restore them, they're a buffer

---

## Death and Dying

### Dropping to 0 HP
You fall unconscious and start making death saving throws.

### Death Saving Throws
At the start of each of your turns while at 0 HP:
- Roll d20 (no modifiers unless you have a feature that adds them)
- 10 or higher: success
- 9 or lower: failure
- **3 successes**: Stabilize (unconscious but no longer dying, regain 1 HP after 1d4 hours)
- **3 failures**: Dead
- **Natural 20**: Regain 1 HP (wake up, back in the fight)
- **Natural 1**: Counts as 2 failures

Successes and failures don't need to be consecutive. Reset when you regain any HP.

### Taking Damage at 0 HP
- Any damage while at 0 HP = automatic death save failure
- A critical hit = 2 failures
- If the damage equals or exceeds your HP maximum, instant death (e.g., a character with 30 max HP at 0 HP takes 30+ damage = dead)

### Instant Death
If damage reduces you to 0 and the remaining damage equals or exceeds your max HP, you die instantly. No death saves. Example: a character with 12 max HP at 8 HP takes 20 damage — drops to 0 with 12 excess damage, which equals max HP. Instant death.

### Stabilizing
A creature can stabilize a dying character with a DC 10 WIS (Medicine) check (action). Spare the Dying cantrip does it automatically. Healer's kit does it without a check.

---

## Movement in Combat

### Normal Movement
Move up to your speed on your turn. Can split movement before and after actions.

### Difficult Terrain
Every foot of movement costs 1 extra foot. 30 ft speed = 15 ft of movement in difficult terrain.

### Prone
- Dropping prone: free (no movement cost)
- Standing up: costs half your movement speed
- While prone: disadvantage on attack rolls, melee attacks against you have advantage, ranged attacks against you have disadvantage
- Crawling while prone: 1 extra foot per foot moved

### Jumping
- **Long jump**: Running = STR score in feet. Standing = half that.
- **High jump**: Running = 3 + STR modifier in feet. Standing = half that.

### Climbing, Swimming
Costs 1 extra foot per foot moved (like difficult terrain). In difficult terrain while climbing/swimming, costs 2 extra feet per foot.

### Flying
Creatures with a fly speed fall if knocked prone, their speed is reduced to 0, or they're otherwise deprived of movement (unless they can hover).

---

## Cover

| Cover | AC/DEX Save Bonus | Example |
|-------|-------------------|---------|
| Half (+2) | +2 | Low wall, furniture, another creature |
| Three-quarters (+5) | +5 | Portcullis, arrow slit, thick tree trunk |
| Total | Can't be targeted directly | Completely concealed behind wall |

A creature behind another creature of the same size or larger has at minimum half cover.

---

## Grappling

**Initiate**: Replace one attack with a grapple attempt. STR (Athletics) check vs. target's STR (Athletics) or DEX (Acrobatics).

**Effect**: Grappled creature's speed becomes 0. Grappler can drag/carry the target at half speed.

**Escape**: Target uses action to make STR (Athletics) or DEX (Acrobatics) vs. grappler's STR (Athletics).

**Shove**: Similar to grapple — replace one attack, contested check. Push target 5 ft away or knock them prone.

**Grapple + Shove Prone combo**: Grapple first (speed = 0), then shove prone. Target can't stand up because standing costs movement and their speed is 0. They're stuck prone with disadvantage on attacks and advantage on melee attacks against them. Strong martial tactic.

---

## Mounted Combat

- Mounting/dismounting costs half your movement
- While mounted, you can use the mount's speed instead of yours
- **Controlled mount** (trained, like a warhorse): Shares your initiative. Can only Dash, Disengage, or Dodge. Can't attack.
- **Independent mount** (intelligent creature, wild beast): Keeps its own initiative and acts normally
- If mount is forced to move, rider makes DC 10 DEX save or falls prone 5 ft from mount
- If knocked prone while mounted, same save — or dismount on your feet (reaction)

---

## Underwater Combat

- Melee attacks with non-piercing weapons: disadvantage (unless creature has swim speed)
- Ranged weapon attacks: auto-miss beyond normal range. Disadvantage at normal range (unless crossbow, net, or thrown weapon like javelin/trident)
- Creatures fully submerged have resistance to fire damage
- Holding breath: 1 + CON modifier minutes (minimum 30 seconds). After that, survive for CON modifier rounds (minimum 1), then drop to 0 HP
