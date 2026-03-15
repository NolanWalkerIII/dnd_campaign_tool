# Character Creation

Step-by-step process for building a 5e character. An LLM acting as player assistant should walk through these in order.

## Step 1: Choose a Race

See `04_RACES_REFERENCE.md` for full race details. Race determines:
- Ability Score Increases (ASIs)
- Size and speed
- Racial traits (darkvision, resistances, proficiencies, etc.)
- Languages

## Step 2: Choose a Class

See `03_CLASSES_REFERENCE.md` for full class details. Class determines:
- Hit die (affects HP)
- Saving throw proficiencies
- Skill proficiency options
- Armor and weapon proficiencies
- Class features and progression
- Spellcasting (if applicable)
- Subclass options (gained at level 1, 2, or 3 depending on class)

## Step 3: Determine Ability Scores

Three common methods:

### Standard Array
`15, 14, 13, 12, 10, 8` — assign one to each ability score. No randomness, balanced, good default.

### Point Buy
Start with all scores at 8. You have 27 points to spend.

| Score | Cost |
|-------|------|
| 8 | 0 |
| 9 | 1 |
| 10 | 2 |
| 11 | 3 |
| 12 | 4 |
| 13 | 5 |
| 14 | 7 |
| 15 | 9 |

Max score before racial bonuses: 15. Min: 8. This is the most balanced method for optimized builds.

### Rolling
Roll 4d6, drop the lowest die, six times. Assign to abilities as desired. Higher variance — can produce very strong or very weak characters. Some tables reroll if total modifiers sum is below a threshold (e.g., +3 total).

### Where to Put Scores

General priority for common archetypes:
- **Martial (Fighter, Barbarian, Paladin)**: STR or DEX first, CON second
- **Full Casters (Wizard, Cleric, Druid, Sorcerer, Bard, Warlock)**: Casting stat first, CON or DEX second
- **Half Casters (Ranger, Paladin)**: Primary combat stat and casting stat both matter
- **Skill Monkeys (Rogue, Bard)**: DEX and CHA, with decent WIS for Perception

## Step 4: Describe Your Character

### Background

Background provides:
- 2 skill proficiencies
- Tool proficiencies and/or languages
- Starting equipment
- A feature (mostly narrative/RP utility)
- Personality traits, ideals, bonds, and flaws

SRD backgrounds: Acolyte. The full PHB includes ~15 backgrounds (Soldier, Criminal, Noble, Sage, etc.). Custom backgrounds are allowed RAW — pick any 2 skills, 2 tool/language proficiencies, and a feature.

### Alignment

Two-axis system: Law/Neutral/Chaos × Good/Neutral/Evil = 9 options.

| | Good | Neutral | Evil |
|---|------|---------|------|
| Lawful | LG | LN | LE |
| Neutral | NG | N (True Neutral) | NE |
| Chaotic | CG | CN | CE |

Alignment is a descriptive shorthand, not a behavioral straitjacket. Many tables barely reference it. Useful as a starting point for roleplaying, not a rule.

### Personal Characteristics

Each character should have:
- **Personality Traits** (2): How they act and present themselves
- **Ideals** (1): What they believe in, what drives them
- **Bonds** (1): Connections to people, places, or things
- **Flaws** (1): Weaknesses, vices, fears

These are the primary hooks for roleplay and narrative. An LLM playing DM should reference these when creating story hooks and NPC interactions.

## Step 5: Choose Equipment

Two options:
1. **Class starting equipment** — predefined packages listed in class description
2. **Starting gold** — roll gold based on class, buy gear from equipment lists

| Class | Starting Gold (if rolling) |
|-------|---------------------------|
| Barbarian | 2d4 × 10 gp |
| Bard | 5d4 × 10 gp |
| Cleric | 5d4 × 10 gp |
| Druid | 2d4 × 10 gp |
| Fighter | 5d4 × 10 gp |
| Monk | 5d4 gp |
| Paladin | 5d4 × 10 gp |
| Ranger | 5d4 × 10 gp |
| Rogue | 4d4 × 10 gp |
| Sorcerer | 3d4 × 10 gp |
| Warlock | 4d4 × 10 gp |
| Wizard | 4d4 × 10 gp |

See `09_EQUIPMENT.md` for full price lists.

## Step 6: Calculate Derived Stats

### Hit Points
```
Level 1 HP = hit die maximum + CON modifier
```
Each level after 1st: roll hit die (or take average) + CON modifier.

Average values per hit die: d6 = 4, d8 = 5, d10 = 6, d12 = 7.

### Armor Class
Depends on armor worn. See `09_EQUIPMENT.md` for armor table.
- **No armor**: 10 + DEX modifier
- **Light armor**: armor base + DEX modifier
- **Medium armor**: armor base + DEX modifier (max +2)
- **Heavy armor**: armor base (DEX doesn't apply)
- **Shield**: +2 AC on top of armor

Some classes/races have alternate AC calculations (Monk: 10 + DEX + WIS, Barbarian: 10 + DEX + CON, Draconic Sorcerer: 13 + DEX).

### Initiative
```
Initiative = DEX modifier (+ any special bonuses)
```

### Speed
Determined by race. Most medium races: 30 ft. Dwarves and halflings: 25 ft.

### Proficiencies
Compiled from race + class + background. No duplicates — if two sources give the same skill, some classes let you pick a replacement.

## Step 7: Spellcasting (if applicable)

If the class has spellcasting:
1. Determine spellcasting ability (class-dependent)
2. Calculate spell save DC and spell attack modifier (see `01_CORE_MECHANICS.md`)
3. Determine known/prepared spells and cantrips (class-specific rules)
4. Note spell slot progression (see `06_SPELLCASTING.md`)

## Level Up Checklist

When a character gains a level:
1. Check for new class features
2. Check for subclass features
3. Increase HP (roll or take average + CON mod)
4. Check if proficiency bonus increases (levels 5, 9, 13, 17)
5. Check for Ability Score Improvement (typically levels 4, 8, 12, 16, 19)
6. Update spell slots and known/prepared spells if applicable
7. Fighter gets extra ASIs at 6 and 14. Rogue gets one at 10.
