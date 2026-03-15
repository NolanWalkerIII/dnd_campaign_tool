# Classes Reference

All 12 PHB classes. Each entry covers hit die, primary abilities, saving throw proficiencies, armor/weapon proficiencies, core features, and subclass timing.

## Quick Reference Table

| Class | Hit Die | Primary Ability | Saves | Armor | Spellcasting |
|-------|---------|----------------|-------|-------|-------------|
| Barbarian | d12 | STR | STR, CON | Light, Medium, Shields | None |
| Bard | d8 | CHA | DEX, CHA | Light | Full (CHA) |
| Cleric | d8 | WIS | WIS, CHA | Light, Medium, Shields | Full (WIS) |
| Druid | d8 | WIS | INT, WIS | Light, Medium, Shields (nonmetal) | Full (WIS) |
| Fighter | d10 | STR or DEX | STR, CON | All armor, Shields | None (EK: Third) |
| Monk | d8 | DEX & WIS | STR, DEX | None | None |
| Paladin | d10 | STR & CHA | WIS, CHA | All armor, Shields | Half (CHA) |
| Ranger | d10 | DEX & WIS | STR, DEX | Light, Medium, Shields | Half (WIS) |
| Rogue | d8 | DEX | DEX, INT | Light | None (AT: Third) |
| Sorcerer | d6 | CHA | CON, CHA | None | Full (CHA) |
| Warlock | d8 | CHA | WIS, CHA | Light | Pact Magic (CHA) |
| Wizard | d6 | INT | INT, WIS | None | Full (INT) |

---

## Barbarian

**Subclass at**: Level 3 (Primal Path)
**SRD Subclass**: Path of the Berserker

### Core Features
- **Rage** (Level 1): Bonus action to enter rage. Advantage on STR checks/saves, bonus rage damage on melee STR attacks, resistance to bludgeoning/piercing/slashing damage. Lasts 1 minute, ends early if you don't attack or take damage. Can't cast spells while raging. Limited uses per long rest (2 at level 1, scaling to 6+unlimited at 20).
- **Unarmored Defense** (Level 1): AC = 10 + DEX mod + CON mod when not wearing armor.
- **Reckless Attack** (Level 2): First attack on your turn can be made with advantage (STR-based melee). Tradeoff: attack rolls against you have advantage until your next turn.
- **Danger Sense** (Level 2): Advantage on DEX saving throws against effects you can see (traps, spells). Doesn't work if blinded, deafened, or incapacitated.
- **Extra Attack** (Level 5): Two attacks per Attack action.
- **Fast Movement** (Level 5): +10 ft speed when not wearing heavy armor.
- **Brutal Critical** (Level 9/13/17): Extra damage dice on critical hits (1/2/3 additional dice).

### Key ASI/Feat Levels
4, 8, 12, 16, 19

---

## Bard

**Subclass at**: Level 3 (Bard College)
**SRD Subclass**: College of Lore

### Core Features
- **Spellcasting** (Level 1): Full caster, CHA-based. Known spells (not prepared). Ritual casting if spell is known.
- **Bardic Inspiration** (Level 1): Bonus action, give an ally a Bardic Inspiration die (d6, scaling to d12 at level 15). Ally adds the die to one ability check, attack roll, or saving throw within 10 minutes. Uses = CHA modifier per short rest (level 5+) or long rest (before level 5).
- **Jack of All Trades** (Level 2): Add half proficiency bonus (rounded down) to any ability check you're not already proficient in. Applies to initiative.
- **Song of Rest** (Level 2): During short rest, allies who spend Hit Dice regain extra HP (d6, scaling).
- **Expertise** (Level 3, 10): Double proficiency bonus on 2 skills (4 total at level 10).
- **Magical Secrets** (Level 10, 14, 18): Learn 2 spells from any class spell list. This is what makes high-level Bards so flexible.

### Key ASI/Feat Levels
4, 8, 12, 16, 19

---

## Cleric

**Subclass at**: Level 1 (Divine Domain)
**SRD Subclass**: Life Domain

### Core Features
- **Spellcasting** (Level 1): Full caster, WIS-based. Prepares spells each long rest from the full Cleric spell list. Ritual casting if spell is prepared. Gets domain spells always prepared for free.
- **Channel Divinity** (Level 2): 1 use per short rest (2 at level 6, 3 at level 18). All clerics get Turn Undead. Domain grants a second option.
  - **Turn Undead**: Each undead within 30 ft makes WIS save or is turned for 1 minute (flees, can't approach within 30 ft). At higher levels, weak undead are destroyed outright.
- **Divine Intervention** (Level 10): Once per long rest, plead for divine aid. Roll d100 — if roll ≤ cleric level, the DM chooses an appropriate effect (replicate a cleric spell, etc.). Auto-succeeds at level 20. Flavorful but unreliable until 20.

### Key ASI/Feat Levels
4, 8, 12, 16, 19

---

## Druid

**Subclass at**: Level 2 (Druid Circle)
**SRD Subclass**: Circle of the Land

### Core Features
- **Spellcasting** (Level 1): Full caster, WIS-based. Prepares spells each long rest from full Druid list. Ritual casting if prepared.
- **Druidic** (Level 1): Secret language. Can leave hidden messages for other druids.
- **Wild Shape** (Level 2): Use an action to transform into a beast you've seen. 2 uses per short rest. Duration = level/2 hours. CR limits: 1/4 at level 2, 1/2 at level 4, 1 at level 8. No flying until level 8, no swimming until level 4. Your game stats are replaced by the beast's, but you keep INT, WIS, CHA, and your proficiencies. When beast HP drops to 0, you revert with leftover damage carrying over.
- **Beast Spells** (Level 18): Can cast spells in Wild Shape form. This is where Moon Druid gets really nasty.

### Metal Restriction
Druids traditionally won't wear metal armor or shields. This is a flavor restriction, not a mechanical prohibition — no mechanical penalty RAW. But most DMs enforce it.

### Key ASI/Feat Levels
4, 8, 12, 16, 19

---

## Fighter

**Subclass at**: Level 3 (Martial Archetype)
**SRD Subclass**: Champion

### Core Features
- **Fighting Style** (Level 1): Choose one — Archery (+2 ranged attacks), Defense (+1 AC in armor), Dueling (+2 damage one-handed), Great Weapon Fighting (reroll 1s and 2s on damage with two-handed), Protection (impose disadvantage on attack against adjacent ally with shield), Two-Weapon Fighting (add ability mod to off-hand damage).
- **Second Wind** (Level 1): Bonus action, regain 1d10 + fighter level HP. Once per short rest.
- **Action Surge** (Level 2): Take one additional action on your turn. Once per short rest (twice at 17). This is why Fighter multiclass dips are popular — an extra full action is enormous.
- **Extra Attack** (Level 5, 11, 20): 2 attacks at 5, 3 at 11, 4 at 20. Only class that gets 4 attacks.
- **Indomitable** (Level 9, 13, 17): Reroll a failed saving throw. 1/2/3 uses per long rest.

### Key ASI/Feat Levels
4, 6, 8, 12, 14, 16, 19 — Fighters get the most ASIs. This is a big deal for feat-heavy builds.

---

## Monk

**Subclass at**: Level 3 (Monastic Tradition)
**SRD Subclass**: Way of the Open Hand

### Core Features
- **Unarmored Defense** (Level 1): AC = 10 + DEX mod + WIS mod when wearing no armor, no shield.
- **Martial Arts** (Level 1): Use DEX for unarmed strikes and monk weapons. Unarmed strike damage starts at d4, scales to d10 at level 17. When you take the Attack action with an unarmed strike or monk weapon, make one unarmed strike as a bonus action.
- **Ki** (Level 2): Resource pool = monk level. Recharges on short rest.
  - **Flurry of Blows**: 1 ki, bonus action, two unarmed strikes after Attack action.
  - **Patient Defense**: 1 ki, bonus action, take Dodge action.
  - **Step of the Wind**: 1 ki, bonus action, Disengage or Dash plus doubled jump distance.
- **Unarmored Movement** (Level 2): +10 ft speed without armor (scales to +30 ft at level 18). Can run on water/vertical surfaces at level 9 (only during movement, fall if you stop).
- **Deflect Missiles** (Level 3): Reduce ranged weapon damage by 1d10 + DEX mod + monk level. If reduced to 0, catch it and throw it back for 1 ki.
- **Stunning Strike** (Level 5): On hit with melee, spend 1 ki — target makes CON save or is stunned until end of your next turn. This is the monk's most impactful ability.
- **Evasion** (Level 7): DEX saves for half damage become no damage on success, half on failure.

### Key ASI/Feat Levels
4, 8, 12, 16, 19

---

## Paladin

**Subclass at**: Level 3 (Sacred Oath)
**SRD Subclass**: Oath of Devotion

### Core Features
- **Divine Sense** (Level 1): Know location of celestials, fiends, and undead within 60 ft. 1 + CHA mod uses per long rest.
- **Lay on Hands** (Level 1): Pool of HP = paladin level × 5. Touch a creature to restore HP from the pool, or spend 5 points to cure a disease or neutralize a poison. The most efficient healing in the game at low levels.
- **Fighting Style** (Level 2): Same options as Fighter minus Archery and Two-Weapon Fighting.
- **Spellcasting** (Level 2): Half caster, CHA-based. Prepares spells from Paladin list. Gets oath spells always prepared.
- **Divine Smite** (Level 2): On a melee weapon hit, expend a spell slot to deal extra 2d8 radiant damage (+1d8 per slot level above 1st, max 5d8). +1d8 against undead or fiend. You can decide to smite after seeing the hit, which is what makes it so strong — you can save slots for critical hits (double the smite dice).
- **Aura of Protection** (Level 6): You and allies within 10 ft (30 ft at level 18) add your CHA modifier to all saving throws. This is arguably the strongest level 6 feature in the game.
- **Extra Attack** (Level 5): Two attacks per Attack action.

### Key ASI/Feat Levels
4, 8, 12, 16, 19

---

## Ranger

**Subclass at**: Level 3 (Ranger Archetype)
**SRD Subclass**: Hunter

### Core Features
- **Favored Enemy** (Level 1): Advantage on WIS (Survival) checks to track chosen enemy type, INT checks to recall info about them. Extra language. Additional enemy types at 6 and 14. (Widely considered underpowered — many tables use revised ranger or Tasha's optional features.)
- **Natural Explorer** (Level 1): In favored terrain, the party can't become lost except by magic, stays alert while doing other activities, moves stealthily at normal pace, finds twice as much food foraging, and learns exact numbers/sizes of tracked creatures. Additional terrains at 6 and 10.
- **Fighting Style** (Level 2): Archery, Defense, Dueling, or Two-Weapon Fighting.
- **Spellcasting** (Level 2): Half caster, WIS-based. Known spells (not prepared).
- **Extra Attack** (Level 5): Two attacks per Attack action.
- **Land's Stride** (Level 8): Move through nonmagical difficult terrain with no extra movement cost. Advantage on saves vs. magically created plants (Entangle, Spike Growth, etc.).

### Tasha's Optional Features (widely adopted)
Replaces Favored Enemy and Natural Explorer with Favored Foe (bonus damage on concentration) and Deft Explorer (expertise, languages, climbing/swimming speed). Much better mechanically.

### Key ASI/Feat Levels
4, 8, 12, 16, 19

---

## Rogue

**Subclass at**: Level 3 (Roguish Archetype)
**SRD Subclass**: Thief

### Core Features
- **Expertise** (Level 1, 6): Double proficiency on 2 skills at each level (4 total).
- **Sneak Attack** (Level 1): Once per turn, add extra dice to one attack with a finesse or ranged weapon. Requires advantage on the attack OR an enemy of the target within 5 ft of it. Starts at 1d6, gains 1d6 every 2 rogue levels (10d6 at 19). This is the bulk of Rogue damage.
- **Thieves' Cant** (Level 1): Secret language. Mix of dialect, code words, and symbols.
- **Cunning Action** (Level 2): Use bonus action to Dash, Disengage, or Hide. This is what makes Rogues so mobile and slippery.
- **Uncanny Dodge** (Level 5): Reaction to halve damage from an attack you can see.
- **Evasion** (Level 7): Same as Monk — DEX save half becomes zero, fail becomes half.
- **Reliable Talent** (Level 11): Any ability check that uses proficiency — treat any d20 roll of 9 or lower as a 10. The floor on your skill checks becomes very high.

### Key ASI/Feat Levels
4, 8, 10, 12, 16, 19 — Rogue gets an extra ASI at 10.

---

## Sorcerer

**Subclass at**: Level 1 (Sorcerous Origin)
**SRD Subclass**: Draconic Bloodline

### Core Features
- **Spellcasting** (Level 1): Full caster, CHA-based. Known spells (very limited list — fewer known than any other full caster).
- **Font of Magic / Sorcery Points** (Level 2): Pool = sorcerer level. Can convert spell slots to points and vice versa. Main use is fueling Metamagic.
  - Slot to points: slot level = points gained.
  - Points to slot: 2 pts = 1st, 3 = 2nd, 5 = 3rd, 6 = 4th, 7 = 5th. Can't create slots above 5th.
- **Metamagic** (Level 3): Choose 2 options (more at 10, 17). Apply to spells for sorcery point cost.
  - **Twinned Spell**: Target a second creature with a single-target spell. Cost = spell level (1 for cantrips).
  - **Quickened Spell**: Cast a spell as a bonus action instead of an action. 2 points. Remember: if you cast a bonus action spell, your action can only be used for a cantrip.
  - **Subtle Spell**: No verbal or somatic components. 1 point. Can't be counterspelled. Great for social situations.
  - **Heightened Spell**: One target has disadvantage on first save against the spell. 3 points.
  - **Empowered Spell**: Reroll up to CHA mod damage dice and use new rolls. 1 point.
  - **Extended Spell**: Double duration (max 24 hours). 1 point.
  - **Careful Spell**: Choose CHA mod creatures — they auto-succeed on the spell's save. 1 point. Note: they still take half damage from spells that deal half on a success.
  - **Distant Spell**: Double range (or 30 ft if touch). 1 point.

### Key ASI/Feat Levels
4, 8, 12, 16, 19

---

## Warlock

**Subclass at**: Level 1 (Otherworldly Patron)
**SRD Subclass**: The Fiend

### Core Features
- **Pact Magic** (Level 1): CHA-based. Unique spellcasting — very few slots (1-4), but they're all cast at the highest available level and recharge on short rest. Slot level scales from 1st (level 1) to 5th (level 9+).
- **Eldritch Invocations** (Level 2): Customizable abilities. Choose from a list that grows as you level. Key invocations:
  - **Agonizing Blast**: Add CHA mod to Eldritch Blast damage. Essentially mandatory.
  - **Repelling Blast**: Push targets 10 ft on Eldritch Blast hit. No save.
  - **Devil's Sight**: See normally in magical and nonmagical darkness to 120 ft. Combos with the Darkness spell.
  - **Book of Ancient Secrets** (Pact of the Tome): Ritual casting from any class.
  - **Mask of Many Faces**: At-will Disguise Self.
- **Pact Boon** (Level 3): Choose one:
  - **Pact of the Chain**: Improved familiar (imp, pseudodragon, quasit, sprite).
  - **Pact of the Blade**: Conjure a melee weapon, use CHA for attacks (with Hexblade or invocations).
  - **Pact of the Tome**: Book with 3 cantrips from any class.
- **Mystic Arcanum** (Levels 11, 13, 15, 17): One spell each of 6th, 7th, 8th, 9th level. Cast once per long rest each. Not a slot — just a single cast.

### Eldritch Blast
The Warlock's signature cantrip. 1d10 force damage, 120 ft range. Gains extra beams at levels 5, 11, 17 (matching cantrip scaling). Each beam can target separately. With Agonizing Blast, this is competitive with martial damage output.

### Key ASI/Feat Levels
4, 8, 12, 16, 19

---

## Wizard

**Subclass at**: Level 2 (Arcane Tradition)
**SRD Subclass**: School of Evocation

### Core Features
- **Spellcasting** (Level 1): Full caster, INT-based. Prepares spells from spellbook. Largest spell list in the game. Ritual casting if spell is in spellbook (doesn't need to be prepared).
- **Arcane Recovery** (Level 1): Once per day during short rest, recover spell slots with combined level ≤ half wizard level (rounded up). No slots above 6th.
- **Spellbook**: The wizard's defining mechanic. Starts with 6 first-level spells. Gains 2 free spells per level. Can copy spells found on scrolls or other spellbooks (2 hours and 50 gp per spell level). This means wizards get dramatically more spell options than any other class if the DM provides scrolls/spellbooks as loot.
- **Spell Mastery** (Level 18): Choose one 1st-level and one 2nd-level spell in your spellbook. Cast them at their lowest level without expending a slot.
- **Signature Spells** (Level 20): Two 3rd-level spells always prepared, each castable once per short rest without a slot.

### Key ASI/Feat Levels
4, 8, 12, 16, 19

---

## Multiclassing

### Prerequisites
Must have 13+ in the primary ability of both your current class and the new class.

| Class | Prerequisite |
|-------|-------------|
| Barbarian | STR 13 |
| Bard | CHA 13 |
| Cleric | WIS 13 |
| Druid | WIS 13 |
| Fighter | STR 13 or DEX 13 |
| Monk | DEX 13 and WIS 13 |
| Paladin | STR 13 and CHA 13 |
| Ranger | DEX 13 and WIS 13 |
| Rogue | DEX 13 |
| Sorcerer | CHA 13 |
| Warlock | CHA 13 |
| Wizard | INT 13 |

### Proficiencies Gained from Multiclassing
You don't get all proficiencies of the new class — you get a reduced set. Notably, you never gain saving throw proficiencies from multiclassing.

### Spell Slot Calculation for Multiclass Casters
Add together: full caster levels + half your half-caster levels (rounded down) + one-third your third-caster levels (rounded down). Look up the total on the multiclass spellcaster table. Warlock Pact Magic slots are tracked separately and don't combine.

### Common Multiclass Dips
- **Fighter 1-2**: Armor proficiencies, CON save, Fighting Style, Action Surge
- **Hexblade Warlock 1-2**: CHA to attacks, medium armor, shield, Eldritch Blast + Agonizing Blast
- **Cleric 1**: Armor proficiencies, WIS save, domain features (Peace, Twilight are strong)
- **Rogue 1-3**: Expertise, Sneak Attack, Cunning Action
- **Paladin 2**: Divine Smite on a CHA-based character
