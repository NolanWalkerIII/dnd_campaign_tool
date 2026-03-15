# Monster Guide

## Stat Block Anatomy

Every monster follows the same stat block format. An LLM needs to understand each field to run monsters correctly.

```
MONSTER NAME
Size Type (subtype), Alignment
───────────────────────────────
Armor Class: [AC value] ([armor type])
Hit Points: [average] ([dice expression])
Speed: [walk] ft., [fly/swim/climb/burrow] ft.
───────────────────────────────
STR     DEX     CON     INT     WIS     CHA
[score] [score] [score] [score] [score] [score]
([mod]) ([mod]) ([mod]) ([mod]) ([mod]) ([mod])
───────────────────────────────
Saving Throws: [ability +bonus, ...]
Skills: [skill +bonus, ...]
Damage Resistances: [types]
Damage Immunities: [types]
Condition Immunities: [conditions]
Senses: [darkvision Xft, passive Perception X]
Languages: [languages]
Challenge: [CR] ([XP] XP)
───────────────────────────────
TRAITS
[Name.] [Description]

ACTIONS
[Name.] [Attack type]: +[bonus] to hit, reach/range [X] ft., [targets]. Hit: [damage] [type] damage.

REACTIONS (if any)
[Name.] [Description]

LEGENDARY ACTIONS (if any)
The [monster] can take [X] legendary actions, choosing from the options below. Only one legendary action can be used at a time and only at the end of another creature's turn. The [monster] regains spent legendary actions at the start of its turn.
```

### Key Fields for LLM

- **AC and HP**: AC is the attack target number. HP determines how much damage the monster can take. Use the average HP for consistency, or roll the dice expression for variance.
- **Speed**: Multiple movement types are common. A creature with "30 ft., fly 60 ft." can walk 30 or fly 60 (or mix).
- **Saving Throw Proficiencies**: Only listed throws have proficiency. All others use raw ability modifier.
- **Senses**: Passive Perception is used for spotting hidden characters. Darkvision, blindsight, tremorsense, and truesight affect what the creature can detect.
- **Challenge Rating (CR)**: Rough indicator of difficulty. See encounter building section below.

---

## Monster Types

| Type | Description | Typical Examples |
|------|-------------|-----------------|
| Aberration | Alien, unnatural beings | Beholder, Mind Flayer, Aboleth |
| Beast | Nonmagical animals | Wolf, Bear, Giant Eagle |
| Celestial | Beings from upper planes | Angel, Unicorn, Pegasus |
| Construct | Magically created beings | Golem, Animated Armor, Shield Guardian |
| Dragon | Winged reptilian creatures | Chromatic and metallic dragons, wyvern |
| Elemental | Beings from elemental planes | Fire Elemental, Water Elemental, Djinni |
| Fey | Creatures tied to the Feywild | Dryad, Satyr, Sprite, Hag |
| Fiend | Beings from lower planes | Demon, Devil, Balor, Pit Fiend |
| Giant | Humanoids of great size | Hill Giant, Storm Giant, Ogre, Troll |
| Humanoid | Human-like creatures | Bandits, goblins, orcs, kobolds |
| Monstrosity | Unnatural creatures not fitting other types | Owlbear, Mimic, Manticore, Bulette |
| Ooze | Amorphous, acidic creatures | Gelatinous Cube, Black Pudding |
| Plant | Vegetable creatures | Treant, Shambling Mound, Myconid |
| Undead | Once-living, animated by dark magic | Zombie, Skeleton, Vampire, Lich |

Type matters for features like Favored Enemy, Turn Undead, Divine Smite bonus, and certain spells that only affect specific types (Hold Person = humanoids only).

---

## Challenge Rating (CR)

CR is a rough estimate of how dangerous a monster is. A monster of CR X should be a medium challenge for a party of 4 characters of level X.

### CR to XP Table

| CR | XP | Proficiency |
|----|-----|------------|
| 0 | 0-10 | +2 |
| 1/8 | 25 | +2 |
| 1/4 | 50 | +2 |
| 1/2 | 100 | +2 |
| 1 | 200 | +2 |
| 2 | 450 | +2 |
| 3 | 700 | +2 |
| 4 | 1,100 | +2 |
| 5 | 1,800 | +3 |
| 6 | 2,300 | +3 |
| 7 | 2,900 | +3 |
| 8 | 3,900 | +3 |
| 9 | 5,000 | +4 |
| 10 | 5,900 | +4 |
| 11 | 7,200 | +4 |
| 12 | 8,400 | +4 |
| 13 | 10,000 | +5 |
| 14 | 11,500 | +5 |
| 15 | 13,000 | +5 |
| 16 | 15,000 | +5 |
| 17 | 18,000 | +6 |
| 18 | 20,000 | +6 |
| 19 | 22,000 | +6 |
| 20 | 25,000 | +6 |
| 21 | 33,000 | +7 |
| 22 | 41,000 | +7 |
| 23 | 50,000 | +7 |
| 24 | 62,000 | +7 |
| 25 | 75,000 | +8 |
| 26 | 90,000 | +8 |
| 27 | 105,000 | +8 |
| 28 | 120,000 | +8 |
| 29 | 135,000 | +9 |
| 30 | 155,000 | +9 |

### Monster XP Multiplier (for encounter building)
When there are multiple monsters, the effective XP is multiplied:

| Number of Monsters | Multiplier |
|-------------------|-----------|
| 1 | × 1 |
| 2 | × 1.5 |
| 3-6 | × 2 |
| 7-10 | × 2.5 |
| 11-14 | × 3 |
| 15+ | × 4 |

This multiplier accounts for action economy — more monsters means more turns, which is disproportionately dangerous.

---

## Common Monster Traits

### Universal Traits
- **Pack Tactics**: Advantage on attack if an ally is within 5 ft of target. Wolves, kobolds.
- **Keen Senses**: Advantage on Perception checks using a specific sense (smell, sight, hearing).
- **Magic Resistance**: Advantage on saves against spells and magical effects. Very strong.
- **Legendary Resistance** (X/Day): If the creature fails a save, it can choose to succeed instead. Boss monsters use this to avoid getting locked down by a single failed save.
- **Innate Spellcasting**: Can cast certain spells without material components, using a specified ability.
- **Spellcasting**: Full spell list and slots, just like a PC caster.
- **Multiattack**: Makes multiple attacks on its turn (described in Actions).
- **Regeneration**: Regains HP at start of turn unless a specified condition is met (fire/acid damage for trolls, for example).

### Damage Immunities / Resistances (Common Patterns)
- **Undead**: Often immune to poison, necrotic. Resistant to nonmagical physical.
- **Fiends**: Often resistant to cold, fire, lightning. Immune to poison. Resistant to nonmagical physical.
- **Constructs**: Often immune to poison, psychic. Immune to charmed, exhaustion, frightened.
- **Elementals**: Immune to poison. Often resistant or immune to their element.

---

## Example Stat Blocks

### Goblin (CR 1/4)
```
Small Humanoid (Goblinoid), Neutral Evil
AC: 15 (leather armor, shield)
HP: 7 (2d6)
Speed: 30 ft.

STR 8(-1) DEX 14(+2) CON 10(+0) INT 10(+0) WIS 8(-1) CHA 8(-1)

Skills: Stealth +6
Senses: Darkvision 60 ft., Passive Perception 9
Languages: Common, Goblin
CR: 1/4 (50 XP)

Nimble Escape. Disengage or Hide as a bonus action on each turn.

ACTIONS
Scimitar. Melee: +4 to hit, reach 5 ft., one target. Hit: 5 (1d6+2) slashing.
Shortbow. Ranged: +4 to hit, range 80/320 ft., one target. Hit: 5 (1d6+2) piercing.
```

### Wolf (CR 1/4)
```
Medium Beast, Unaligned
AC: 13 (natural armor)
HP: 11 (2d8+2)
Speed: 40 ft.

STR 12(+1) DEX 15(+2) CON 12(+1) INT 3(-4) WIS 12(+1) CHA 6(-2)

Skills: Perception +3, Stealth +4
Senses: Passive Perception 13
Languages: —
CR: 1/4 (50 XP)

Keen Hearing and Smell. Advantage on Perception checks using hearing or smell.
Pack Tactics. Advantage on attack if an ally is within 5 ft of target and ally isn't incapacitated.

ACTIONS
Bite. Melee: +4 to hit, reach 5 ft., one target. Hit: 7 (2d4+2) piercing.
Target must succeed on DC 11 STR save or be knocked prone.
```

### Skeleton (CR 1/4)
```
Medium Undead, Lawful Evil
AC: 13 (armor scraps)
HP: 13 (2d8+4)
Speed: 30 ft.

STR 10(+0) DEX 14(+2) CON 15(+2) INT 6(-2) WIS 8(-1) CHA 5(-3)

Damage Vulnerabilities: Bludgeoning
Damage Immunities: Poison
Condition Immunities: Exhaustion, Poisoned
Senses: Darkvision 60 ft., Passive Perception 9
Languages: Understands languages it knew in life but can't speak
CR: 1/4 (50 XP)

ACTIONS
Shortsword. Melee: +4 to hit, reach 5 ft., one target. Hit: 5 (1d6+2) piercing.
Shortbow. Ranged: +4 to hit, range 80/320 ft., one target. Hit: 5 (1d6+2) piercing.
```

### Bandit Captain (CR 2)
```
Medium Humanoid (any race), Any Non-Lawful
AC: 15 (studded leather)
HP: 65 (10d8+20)
Speed: 30 ft.

STR 15(+2) DEX 16(+3) CON 14(+2) INT 14(+2) WIS 11(+0) CHA 14(+2)

Saving Throws: STR +4, DEX +5, WIS +2
Skills: Athletics +4, Deception +4
Senses: Passive Perception 10
Languages: Any two
CR: 2 (450 XP)

ACTIONS
Multiattack. Three melee attacks: two with scimitar, one with dagger.
Scimitar. Melee: +5 to hit, reach 5 ft., one target. Hit: 6 (1d6+3) slashing.
Dagger. Melee or Ranged: +5 to hit, reach 5 ft. or range 20/60 ft., one target. Hit: 5 (1d4+3) piercing.

REACTIONS
Parry. Add 2 to AC against one melee attack that would hit. Must see attacker and be wielding a melee weapon.
```

### Ogre (CR 2)
```
Large Giant, Chaotic Evil
AC: 11 (hide armor)
HP: 59 (7d10+21)
Speed: 40 ft.

STR 19(+4) DEX 8(-1) CON 16(+3) INT 5(-3) WIS 7(-2) CHA 7(-2)

Senses: Darkvision 60 ft., Passive Perception 8
Languages: Common, Giant
CR: 2 (450 XP)

ACTIONS
Greatclub. Melee: +6 to hit, reach 5 ft., one target. Hit: 13 (2d8+4) bludgeoning.
Javelin. Melee or Ranged: +6 to hit, reach 5 ft. or range 30/120 ft., one target. Hit: 11 (2d6+4) piercing.
```

### Owlbear (CR 3)
```
Large Monstrosity, Unaligned
AC: 13 (natural armor)
HP: 59 (7d10+21)
Speed: 40 ft.

STR 20(+5) DEX 12(+1) CON 17(+3) INT 3(-4) WIS 12(+1) CHA 7(-2)

Skills: Perception +3
Senses: Darkvision 60 ft., Passive Perception 13
Languages: —
CR: 3 (700 XP)

Keen Sight and Smell. Advantage on Perception using sight or smell.

ACTIONS
Multiattack. Two attacks: one beak, one claws.
Beak. Melee: +7 to hit, reach 5 ft., one creature. Hit: 10 (1d10+5) piercing.
Claws. Melee: +7 to hit, reach 5 ft., one target. Hit: 14 (2d8+5) slashing.
```

### Young Red Dragon (CR 10)
```
Large Dragon, Chaotic Evil
AC: 18 (natural armor)
HP: 178 (17d10+85)
Speed: 40 ft., climb 40 ft., fly 80 ft.

STR 23(+6) DEX 10(+0) CON 21(+5) INT 14(+2) WIS 11(+0) CHA 19(+4)

Saving Throws: DEX +4, CON +9, WIS +4, CHA +8
Skills: Perception +8, Stealth +4
Damage Immunities: Fire
Senses: Blindsight 30 ft., Darkvision 120 ft., Passive Perception 18
Languages: Common, Draconic
CR: 10 (5,900 XP)

ACTIONS
Multiattack. Three attacks: one bite, two claws.
Bite. Melee: +10 to hit, reach 10 ft., one target. Hit: 17 (2d10+6) piercing + 3 (1d6) fire.
Claw. Melee: +10 to hit, reach 5 ft., one target. Hit: 13 (2d6+6) slashing.
Fire Breath (Recharge 5-6). 30 ft. cone, 16d6 fire, DC 17 DEX save for half.
```

---

## Creating Custom Monsters (LLM Guidance)

When the LLM needs to create a monster on the fly:

### Step 1: Set Target CR
Use the party's level as a baseline. For a medium encounter, the total CR of all monsters should roughly equal the party's average level.

### Step 2: Use the Monster Statistics by CR Table

| CR | AC | HP | Attack Bonus | Damage/Round | Save DC |
|----|-----|------|-------------|-------------|---------|
| 1/4 | 13 | 7-35 | +3 | 2-5 | 13 |
| 1/2 | 13 | 36-49 | +3 | 6-8 | 13 |
| 1 | 13 | 50-70 | +3 | 9-14 | 13 |
| 2 | 13 | 71-85 | +3 | 15-20 | 13 |
| 3 | 13 | 86-100 | +4 | 21-26 | 13 |
| 4 | 14 | 101-115 | +5 | 27-32 | 14 |
| 5 | 15 | 116-130 | +6 | 33-38 | 15 |
| 6 | 15 | 131-145 | +6 | 39-44 | 15 |
| 7 | 15 | 146-160 | +6 | 45-50 | 15 |
| 8 | 16 | 161-175 | +7 | 51-56 | 16 |
| 9 | 16 | 176-190 | +7 | 57-62 | 16 |
| 10 | 17 | 191-205 | +7 | 63-68 | 16 |

### Step 3: Add Flavor
Pick a monster type, damage types, and 1-2 special traits. Don't overload with abilities — 2-3 notable traits is plenty for most encounters.

### Step 4: Validate
Compare to existing monsters of the same CR. The damage output and survivability should be in a similar range.

---

## Lair Actions and Regional Effects

Boss monsters (typically CR 10+) often have lair actions and regional effects.

**Lair Actions**: On initiative count 20 (losing ties), the creature can use one lair action. These are environmental effects — collapsing ceiling, pools of acid erupting, psychic screams, etc. One per round.

**Regional Effects**: Persistent effects in the area around the lair (miles-wide radius). Example: a dragon's lair might cause local water to become poisonous and sulfurous, or a lich's lair might make undead harder to turn within 1 mile. These end when the creature dies or leaves.

---

## Legendary Actions

Legendary creatures (typically CR 10+) get legendary actions — extra things they can do at the end of other creatures' turns.

Rules:
- Usually 3 legendary actions per round
- Each option has a cost (1-3 actions)
- Only one per turn end
- Regained at the start of the creature's turn
- Common options: single attack (1 action), move without provoking (1 action), special ability (2-3 actions)

This mechanic exists because a single monster against a full party gets wrecked by action economy. Legendary actions compensate by giving the boss more turns.
