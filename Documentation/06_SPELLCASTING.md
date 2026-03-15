# Spellcasting Rules

## Spellcasting Basics

### Who Can Cast
Each spellcasting class has a casting ability, which determines spell save DC and attack modifier.

| Class | Casting Ability | Type | Spells Known vs. Prepared |
|-------|----------------|------|--------------------------|
| Bard | CHA | Full caster | Known |
| Cleric | WIS | Full caster | Prepared (from full list) |
| Druid | WIS | Full caster | Prepared (from full list) |
| Paladin | CHA | Half caster | Prepared (from full list) |
| Ranger | WIS | Half caster | Known |
| Sorcerer | CHA | Full caster | Known |
| Warlock | CHA | Pact Magic | Known |
| Wizard | INT | Full caster | Prepared (from spellbook) |
| Eldritch Knight (Fighter) | INT | Third caster | Known |
| Arcane Trickster (Rogue) | INT | Third caster | Known |

**Known casters** (Bard, Sorcerer, Ranger, Warlock): Have a fixed list of spells they know. Can swap one spell when they level up. Limited selection but always available.

**Prepared casters** (Cleric, Druid, Paladin, Wizard): Choose which spells to prepare each long rest. Number prepared = ability modifier + class level (half level for Paladin). Much more flexible day-to-day.

### Spell Save DC and Attack Modifier

```
Spell Save DC = 8 + proficiency bonus + casting ability modifier
Spell Attack Modifier = proficiency bonus + casting ability modifier
```

## Spell Slots

Spell slots are the resource you spend to cast spells. A spell slot is consumed when you cast a spell of that level or higher. Slots recharge on a long rest (short rest for Warlock).

### Full Caster Slot Progression

| Level | 1st | 2nd | 3rd | 4th | 5th | 6th | 7th | 8th | 9th |
|-------|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| 1 | 2 | - | - | - | - | - | - | - | - |
| 2 | 3 | - | - | - | - | - | - | - | - |
| 3 | 4 | 2 | - | - | - | - | - | - | - |
| 4 | 4 | 3 | - | - | - | - | - | - | - |
| 5 | 4 | 3 | 2 | - | - | - | - | - | - |
| 6 | 4 | 3 | 3 | - | - | - | - | - | - |
| 7 | 4 | 3 | 3 | 1 | - | - | - | - | - |
| 8 | 4 | 3 | 3 | 2 | - | - | - | - | - |
| 9 | 4 | 3 | 3 | 3 | 1 | - | - | - | - |
| 10 | 4 | 3 | 3 | 3 | 2 | - | - | - | - |
| 11 | 4 | 3 | 3 | 3 | 2 | 1 | - | - | - |
| 12 | 4 | 3 | 3 | 3 | 2 | 1 | - | - | - |
| 13 | 4 | 3 | 3 | 3 | 2 | 1 | 1 | - | - |
| 14 | 4 | 3 | 3 | 3 | 2 | 1 | 1 | - | - |
| 15 | 4 | 3 | 3 | 3 | 2 | 1 | 1 | 1 | - |
| 16 | 4 | 3 | 3 | 3 | 2 | 1 | 1 | 1 | - |
| 17 | 4 | 3 | 3 | 3 | 2 | 1 | 1 | 1 | 1 |
| 18 | 4 | 3 | 3 | 3 | 3 | 1 | 1 | 1 | 1 |
| 19 | 4 | 3 | 3 | 3 | 3 | 2 | 1 | 1 | 1 |
| 20 | 4 | 3 | 3 | 3 | 3 | 2 | 2 | 1 | 1 |

### Half Caster Slot Progression (Paladin, Ranger)
Use the full caster table but at half your class level (rounded down). A level 5 Paladin has the slots of a level 2 full caster (3 first-level slots). No slots until level 2.

### Third Caster Slot Progression (EK, AT)
One-third class level (rounded down). No slots until level 3.

### Warlock Pact Magic
Completely separate system. 1-4 slots that are always the same level (scaling from 1st at level 1 to 5th at level 9). All slots recharge on short rest. At higher levels (11+), Mystic Arcanum grants one cast each of 6th-9th level spells per long rest.

| Warlock Level | Slots | Slot Level |
|---------------|-------|-----------|
| 1 | 1 | 1st |
| 2 | 2 | 1st |
| 3 | 2 | 2nd |
| 4 | 2 | 2nd |
| 5 | 2 | 3rd |
| 6 | 2 | 3rd |
| 7 | 2 | 4th |
| 8 | 2 | 4th |
| 9 | 2 | 5th |
| 10 | 2 | 5th |
| 11 | 3 | 5th |
| 12 | 3 | 5th |
| 13 | 3 | 5th |
| 14 | 3 | 5th |
| 15 | 3 | 5th |
| 16 | 3 | 5th |
| 17 | 4 | 5th |
| 18 | 4 | 5th |
| 19 | 4 | 5th |
| 20 | 4 | 5th |

## Upcasting

Many spells gain additional effects when cast using a higher-level slot. The spell description will say "At Higher Levels." Examples: Cure Wounds heals an extra 1d8 per slot level above 1st. Fireball deals an extra 1d6 per slot level above 3rd.

## Cantrips

Level 0 spells. Cast at will, no slot required. Damage cantrips scale at levels 5, 11, and 17 (matching proficiency bonus breakpoints, not class level — this matters for multiclassing).

## Spell Components

| Component | Requirement |
|-----------|------------|
| **V (Verbal)** | Must be able to speak. Silenced = can't cast. |
| **S (Somatic)** | Need a free hand. If holding weapon + shield, need War Caster feat or a hand free. |
| **M (Material)** | Specific material components. Can use a component pouch or spellcasting focus instead, UNLESS the material has a listed gold cost or is consumed by the spell. |

### Spellcasting Focus
Replaces non-costly, non-consumed material components. Different classes use different foci:
- Arcane focus (crystal, orb, rod, staff, wand): Sorcerer, Warlock, Wizard
- Holy symbol (amulet, emblem, reliquary): Cleric, Paladin
- Druidic focus (sprig of mistletoe, totem, wooden staff, yew wand): Druid
- Musical instrument: Bard

## Concentration

Many spells require concentration to maintain. Rules:
- Only one concentration spell at a time. Casting a new concentration spell ends the previous one.
- Taking damage forces a CON save to maintain. DC = 10 or half the damage taken, whichever is higher.
- Being incapacitated or killed ends concentration.
- DM can call for a concentration check from environmental disturbances (earthquake, wave, etc.).

The War Caster feat grants advantage on concentration saves. The Resilient (CON) feat adds proficiency bonus. Both are high-priority for casters.

## Ritual Casting

Spells tagged with "Ritual" can be cast without a slot if you add 10 minutes to the casting time. Not all casters can ritual cast:
- **Bard**: Can ritual cast any known spell tagged Ritual.
- **Cleric**: Can ritual cast prepared Ritual spells.
- **Druid**: Can ritual cast prepared Ritual spells.
- **Wizard**: Can ritual cast any Ritual spell in their spellbook (doesn't need to be prepared). This is huge — the Wizard gets free utility from their book.
- **Warlock (Pact of the Tome + Book of Ancient Secrets)**: Can ritual cast and learn rituals from any class.
- Sorcerer, Paladin, Ranger: Cannot ritual cast.

## Spell Ranges

| Range | Description |
|-------|------------|
| Self | Affects you only (or emanates from you) |
| Touch | Must touch the target |
| Specific distance | e.g., 30 ft, 60 ft, 120 ft, 150 ft |
| Sight | Must be able to see the target |
| Unlimited | Works across any distance on the same plane |

## Areas of Effect

| Shape | How It Works |
|-------|-------------|
| **Cone** | Starts at a point and widens. Length = maximum width. |
| **Cube** | Point of origin on one face. |
| **Cylinder** | Point of origin is the center of the top circle. |
| **Line** | Extends from caster in a straight line of specified width. |
| **Sphere** | Expands from a point. Radius specified. |

## Spell Schools

Eight schools of magic. Mostly relevant for Wizard subclasses and some spell interactions (like Detect Magic identifying schools).

| School | Theme | Example Spells |
|--------|-------|---------------|
| Abjuration | Protection, warding | Shield, Counterspell, Dispel Magic |
| Conjuration | Summoning, teleportation | Misty Step, Conjure Animals, Wish |
| Divination | Knowledge, foresight | Detect Magic, Identify, Scrying |
| Enchantment | Mind control, charm | Charm Person, Hold Person, Suggestion |
| Evocation | Energy, damage | Fireball, Lightning Bolt, Healing Word |
| Illusion | Deception, trickery | Minor Illusion, Major Image, Invisibility |
| Necromancy | Death, undead | Animate Dead, Spare the Dying, Raise Dead |
| Transmutation | Transformation, alteration | Polymorph, Haste, Stone Shape |

## Key Spells by Level (SRD Highlights)

### Cantrips (At Will)
- **Eldritch Blast** (Warlock): 1d10 force, 120 ft, scales with character level
- **Fire Bolt**: 1d10 fire, 120 ft
- **Sacred Flame**: DEX save or 1d8 radiant, ignores cover
- **Guidance**: +1d4 to one ability check (concentration)
- **Mage Hand**: Spectral hand, 30 ft range
- **Minor Illusion**: Sound or image
- **Prestidigitation**: Minor magical tricks
- **Spare the Dying**: Stabilize a creature at 0 HP (touch)
- **Toll the Dead**: WIS save or 1d8/1d12 necrotic

### 1st Level
- **Healing Word**: Bonus action, 1d4 + mod healing at 60 ft. The best low-level heal because it's a bonus action at range.
- **Shield**: Reaction, +5 AC until start of next turn
- **Bless**: Concentration, up to 3 creatures add 1d4 to attacks and saves
- **Magic Missile**: Auto-hit 3 darts of 1d4+1 force each
- **Cure Wounds**: 1d8 + mod healing, touch
- **Detect Magic**: Concentration, sense magic within 30 ft for 10 min (ritual)
- **Sleep**: 5d8 HP of creatures fall asleep. No save. Strong at level 1, falls off fast.
- **Thunderwave**: 2d8 thunder, 15 ft cube, CON save or pushed 10 ft
- **Hex** (Warlock): Bonus action, +1d6 necrotic on hits, target has disadvantage on one ability check type

### 2nd Level
- **Spiritual Weapon** (Cleric): Bonus action to attack with floating weapon, 1d8+mod force. No concentration. Great sustained damage.
- **Misty Step**: Bonus action teleport 30 ft
- **Hold Person**: Paralyze a humanoid (WIS save, concentration). Melee attacks are auto-crits against paralyzed targets.
- **Lesser Restoration**: Cure disease, blindness, deafness, paralysis, or poison
- **Pass Without Trace**: +10 to Stealth for the whole party. Concentration. Absurdly good.
- **Moonbeam**: Concentration, 2d10 radiant in a cylinder, moves as action. Forces shapechangers to revert.

### 3rd Level
- **Fireball**: 8d6 fire, 20 ft radius, 150 ft range. The iconic damage spell.
- **Counterspell**: Reaction, negate a spell. Auto-success for equal or lower level, ability check for higher.
- **Revivify**: Bring back a creature dead less than 1 minute. 300 gp diamond consumed. First resurrection spell.
- **Dispel Magic**: End one spell on a target. Auto for equal or lower level, ability check for higher.
- **Haste**: Double speed, +2 AC, extra action (Attack one weapon attack only, Dash, Disengage, Hide, Use an Object). Concentration. If concentration drops, target loses a whole turn (can't move or act).
- **Spirit Guardians** (Cleric): 3d8 radiant/necrotic in 15 ft radius around you. Half speed for enemies. Concentration. The Cleric's primary damage engine.
- **Conjure Animals**: Summon beasts. Action economy powerhouse. 8 wolves is a lot of attacks.

### 4th Level
- **Polymorph**: Turn a creature into a beast of CR ≤ target's level/CR. Concentration. The temp HP sponge — Giant Ape at 157 HP is a favorite.
- **Banishment**: CHA save or banished to a harmless demiplane. Concentration 1 min. If target is from another plane and you maintain concentration, they're gone permanently.
- **Greater Invisibility**: Invisible for 1 minute, concentration. Can attack and remain invisible. Much stronger than regular Invisibility.
- **Dimension Door**: Teleport 500 ft. Can bring one willing creature.

### 5th Level
- **Wall of Force**: Impenetrable, invisible wall. Can create a dome. Concentration 10 min. No save. Arguably the best control spell in the game. Only Disintegrate goes through it.
- **Animate Objects**: 10 tiny objects that attack for 1d4+4 each. Concentration. Ridiculous damage output.
- **Raise Dead**: Resurrect a creature dead up to 10 days. 500 gp diamond.
- **Greater Restoration**: Removes a charm, petrification, curse, ability score reduction, or HP max reduction.
- **Cone of Cold**: 8d8 cold, 60 ft cone. Big AoE, slightly less damage than Fireball but larger area.

### 6th-9th Level (Notable)
- **Heal** (6th): 70 HP restored and cures blindness/deafness/disease
- **Sunbeam** (6th): Concentration, 60 ft line of 6d8 radiant each turn
- **Forcecage** (7th): No concentration, no save. Cage or box. Teleportation requires CHA save to escape.
- **Simulacrum** (7th): Create a copy of a creature at half HP. Has all abilities. No concentration.
- **Feeblemind** (8th): INT save, on fail INT and CHA become 1. Can't cast spells. Devastating.
- **Maze** (8th): No save, target is banished to a maze. Must make DC 20 INT checks to escape. Concentration 10 min.
- **Wish** (9th): Do basically anything. Can replicate any spell of 8th level or lower for free. Going beyond that risks never being able to cast Wish again.
- **True Polymorph** (9th): Transform creature or object permanently after 1 hour of concentration. Turn into anything of appropriate CR/level.

## Identifying Spells

- A character can use their reaction to identify a spell being cast with a DC 15 + spell level Arcana check (Xanathar's rule, widely used).
- Detect Magic reveals the presence and school of magic.
- Identify reveals spells affecting a creature or item (no check needed).
