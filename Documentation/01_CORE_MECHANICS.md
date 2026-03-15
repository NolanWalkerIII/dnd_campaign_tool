# Core Mechanics

## The d20 System

Almost every meaningful action in 5e resolves with a d20 roll + modifiers vs. a target number (DC or AC).

```
d20 + ability modifier + proficiency bonus (if proficient) ≥ target number = success
```

That's the entire engine. Everything else is context for when and how to apply it.

## Ability Scores

Six scores define a character's raw capabilities.

| Ability | Governs | Common Checks |
|---------|---------|---------------|
| **Strength (STR)** | Physical power, carrying capacity | Athletics, melee attack/damage |
| **Dexterity (DEX)** | Agility, reflexes, balance | Acrobatics, Stealth, Sleight of Hand, initiative, AC (light/no armor), ranged attacks |
| **Constitution (CON)** | Health, stamina, endurance | Hit points, concentration saves, resisting poison |
| **Intelligence (INT)** | Memory, reasoning, learning | Arcana, History, Investigation, Nature, Religion |
| **Wisdom (WIS)** | Perception, intuition, willpower | Animal Handling, Insight, Medicine, Perception, Survival |
| **Charisma (CHA)** | Force of personality, social influence | Deception, Intimidation, Performance, Persuasion |

### Ability Modifiers

The modifier is what actually gets used in play. The score itself rarely matters directly.

| Score | Modifier |
|-------|----------|
| 1 | -5 |
| 2-3 | -4 |
| 4-5 | -3 |
| 6-7 | -2 |
| 8-9 | -1 |
| 10-11 | +0 |
| 12-13 | +1 |
| 14-15 | +2 |
| 16-17 | +3 |
| 18-19 | +4 |
| 20 | +5 |

Formula: `modifier = floor((score - 10) / 2)`

## Proficiency Bonus

Scales with total character level, not class level.

| Level | Bonus |
|-------|-------|
| 1-4 | +2 |
| 5-8 | +3 |
| 9-12 | +4 |
| 13-16 | +5 |
| 17-20 | +6 |

Applied to: attack rolls with proficient weapons, saving throws you're proficient in, skill checks you're proficient in, spell attack rolls, spell save DCs.

### Expertise

Some features (Bard, Rogue, certain feats) grant expertise — double the proficiency bonus for specific skills. A level 5 Rogue with expertise in Stealth adds +6 (proficiency +3 × 2) instead of +3.

## Ability Checks

When a character attempts something with a meaningful chance of failure, the DM calls for an ability check.

```
d20 + ability modifier + proficiency bonus (if proficient in relevant skill)
```

### Setting DCs

| Difficulty | DC |
|------------|-----|
| Very Easy | 5 |
| Easy | 10 |
| Medium | 15 |
| Hard | 20 |
| Very Hard | 25 |
| Nearly Impossible | 30 |

DC 15 is the workhorse — use it as the default for anything moderately challenging.

### Passive Checks

Used when no active roll is appropriate (typically Perception and Insight).

```
passive score = 10 + all modifiers that apply
```

Advantage on passive checks adds +5. Disadvantage subtracts -5.

### Contested Checks

Both sides roll. Highest total wins. Ties go to the one being acted upon (the defender or the one maintaining the status quo).

Examples: grappling (Athletics vs. Athletics or Acrobatics), hiding (Stealth vs. Perception), lying (Deception vs. Insight).

## Advantage and Disadvantage

- **Advantage**: Roll 2d20, take the higher result.
- **Disadvantage**: Roll 2d20, take the lower result.

Rules:
- Multiple sources of advantage don't stack — you still roll 2d20.
- If you have both advantage AND disadvantage from any number of sources, they cancel out. Roll normally.
- Advantage/disadvantage apply before any modifiers.

Common sources of advantage: attacking unseen target, Help action, certain spells (Faerie Fire), class features.

Common sources of disadvantage: attacking at long range, restrained condition, near hostile in melee while using ranged, heavy armor without STR requirement met.

## Saving Throws

Forced by spells, traps, environmental effects. The creature being affected rolls.

```
d20 + ability modifier + proficiency bonus (if proficient in that save)
```

Each class grants proficiency in exactly 2 saving throws. One is typically a "strong" save (DEX, CON, WIS) and one a "weak" save (STR, INT, CHA).

### Common Saving Throws by Situation

| Save | Typical Triggers |
|------|-----------------|
| STR | Forced movement, being knocked prone, grapple escapes |
| DEX | Area effects (Fireball, traps), dodging hazards |
| CON | Poison, disease, concentration, death effects |
| INT | Psychic attacks, some illusions |
| WIS | Charm, fear, compulsion effects |
| CHA | Banishment, possession, some planar effects |

DEX, CON, and WIS saves come up the most. Characters without proficiency in these will feel it.

## Natural 1s and 20s

### Attack Rolls Only
- **Natural 20**: Always hits, regardless of AC. Roll damage dice twice (critical hit).
- **Natural 1**: Always misses, regardless of modifiers.

### Ability Checks and Saving Throws
RAW (rules as written): natural 1s and 20s have no special effect on ability checks or saves. A natural 20 on a DC 25 check with a +3 modifier (total 23) still fails. Many tables houserule this — worth establishing at session zero.

## Difficulty Class (DC) for Spells

```
Spell Save DC = 8 + proficiency bonus + spellcasting ability modifier
```

```
Spell Attack Modifier = proficiency bonus + spellcasting ability modifier
```

## Inspiration

DM awards inspiration for good roleplay, creative problem-solving, or playing to character flaws/bonds. A player with inspiration can spend it to gain advantage on one attack roll, saving throw, or ability check. Binary state — you either have it or you don't. Can't stack.
