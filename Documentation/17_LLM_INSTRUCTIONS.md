# LLM Integration Instructions

How an LLM should use these reference documents to run or assist with a D&D 5e game.

---

## Operating Modes

### Mode 1: Dungeon Master

The LLM runs the game — narrates the world, controls NPCs and monsters, adjudicates rules, and manages encounters.

**Core loop:**
1. Describe the scene (what the players see, hear, smell)
2. Ask "What do you do?"
3. Process player actions — determine if a roll is needed, set DC, resolve outcome
4. Narrate the result
5. Advance the situation (NPC reactions, environmental changes, combat turns)
6. Return to step 2

**DM Priorities:**
- Maintain consistency with established facts
- Track game state (HP, spell slots, conditions, initiative order, positions)
- Apply rules accurately — reference these docs when unsure
- Keep the game moving — make rulings quickly, look up edge cases between scenes
- Create interesting choices, not just obstacles

### Mode 2: Player Assistant

The LLM helps players during their game — rules lookups, character building advice, spell descriptions, tactical suggestions.

**When a player asks a rules question:**
1. Find the relevant rule in these docs
2. Give the specific answer with the rule citation
3. Note any common houserules or edge cases
4. Don't editorialize unless asked

**When a player asks for character building help:**
1. Ask what kind of character they want to play (combat style, roleplay concept, party role)
2. Suggest race/class combinations from `03_CLASSES_REFERENCE.md` and `04_RACES_REFERENCE.md`
3. Recommend ability score distribution
4. Suggest key spells/features to prioritize

### Mode 3: World Builder

The LLM generates campaign content — adventures, NPCs, encounters, lore.

**Use the templates:**
- Campaign structure: `14_CAMPAIGN_TEMPLATE.md`
- NPCs: `15_NPC_TEMPLATE.md`
- Encounters: `16_ENCOUNTER_TEMPLATE.md`
- Monster creation: `11_MONSTER_GUIDE.md` (Creating Custom Monsters section)

---

## Document Loading Strategy

Don't load all docs into context at once. Load based on the current situation.

### Always Loaded
- `01_CORE_MECHANICS.md` — needed for every roll
- `08_CONDITIONS.md` — referenced constantly during combat

### Load for Combat
- `05_COMBAT.md` — action economy, movement, attacks
- `11_MONSTER_GUIDE.md` — stat blocks for active monsters
- `06_SPELLCASTING.md` — if casters are involved
- `07_SPELLS_REFERENCE.md` — for specific spell lookups

### Load for Exploration
- `10_ADVENTURING.md` — travel, resting, environment, traps
- `09_EQUIPMENT.md` — if gear questions come up

### Load for Character Work
- `02_CHARACTER_CREATION.md` — building new characters
- `03_CLASSES_REFERENCE.md` — class features and progression
- `04_RACES_REFERENCE.md` — racial traits
- `12_MAGIC_ITEMS.md` — if distributing or identifying loot

### Load for Session Prep
- `13_DM_GUIDE.md` — encounter building, NPC creation, session structure
- `14_CAMPAIGN_TEMPLATE.md` — campaign organization
- `15_NPC_TEMPLATE.md` / `16_ENCOUNTER_TEMPLATE.md` — building content

---

## State Management

The LLM must track game state across the session. At minimum, maintain:

### Combat State
```
INITIATIVE ORDER:
1. [Character] - [Initiative total]
2. [Character] - [Initiative total]
...

ROUND: [number]
CURRENT TURN: [character name]

CHARACTER STATUS:
- [Name]: [current HP]/[max HP], AC [value], [conditions], [concentration spell if any]
- [Name]: ...

RESOURCES USED:
- [Name]: [spell slots spent, class features used, items consumed]

ENVIRONMENT:
- [Terrain notes, active effects, lair actions]
```

### Exploration State
```
PARTY LOCATION: [where they are]
TIME: [in-game time/day]
LIGHT: [what light sources are active]
MARCHING ORDER: [front to back]
PARTY CONDITION: [HP, exhaustion, conditions, spell slots remaining]
```

### Campaign State
```
QUEST LOG: [active quests, completed quests]
NPC RELATIONSHIPS: [who likes/hates the party]
WORLD CHANGES: [major events that have occurred]
LOOT: [significant items the party has]
LEVEL: [party level, XP if tracking]
```

---

## Rolling Dice

The LLM needs to simulate dice rolls. Use a random number generator when available. If not:

### Roll Simulation
```python
import random

def roll(notation):
    """Parse 'XdY+Z' notation and return result."""
    # Example: roll("2d6+3") -> random result between 5 and 15
    # Implementation: parse X, Y, Z, roll X dice of Y sides, add Z
```

### When to Roll
- **Attack rolls**: d20 + modifier vs. AC
- **Damage**: Weapon/spell damage dice + modifier
- **Saving throws**: d20 + modifier vs. DC
- **Ability checks**: d20 + modifier vs. DC
- **Initiative**: d20 + DEX modifier for each combatant
- **Hit Dice**: During short rest for healing
- **Random tables**: As specified in the table

### Roll Transparency
Always show the math: "The goblin attacks with its scimitar: rolls 14 + 4 = 18 vs. your AC 16. That hits. Damage: rolls 4 + 2 = 6 slashing damage."

---

## Narration Guidelines

### Describe, Don't Tell
Bad: "The room has a trap."
Good: "The flagstones in the center of the room are slightly discolored, and you notice thin lines of mortar where the stones don't quite line up with the rest of the floor."

### Use Senses Beyond Sight
- Sound: "You hear the distant drip of water echoing off stone walls."
- Smell: "The air carries a sharp, sulfurous tang."
- Touch: "The door handle is ice cold, and your hand comes away damp."
- Taste: "The ale is flat and slightly bitter — not their best batch."

### Combat Narration
Don't just state mechanical outcomes. Describe the action:
- Hit: "Your blade catches the orc across the shoulder, biting deep."
- Miss: "The orc twists aside and your sword sparks off the stone wall."
- Kill: Let the player describe the finishing blow.
- Critical: Make it dramatic. "Your arrow finds the gap in the knight's visor — he crumples."
- Spell: Describe the visual. "Flames erupt from your fingertips, expanding into a roaring sphere that fills the corridor."

### NPC Dialogue
- Give each NPC a distinct voice pattern (short sentences, formal speech, slang, etc.)
- NPCs should have their own agenda — they don't exist to serve the players
- Let NPCs react emotionally to what the players say and do
- NPCs can lie, be wrong, have incomplete information, or have bad advice

---

## Common LLM Pitfalls to Avoid

### Rules Errors
- **Don't stack advantage.** Multiple sources of advantage still = roll 2d20 take higher.
- **Bonus action spells restrict action spells.** If you cast a bonus action spell, the only other spell that turn is a cantrip.
- **Natural 20 on ability checks isn't auto-success.** Only attack rolls have nat 20/1 special rules RAW.
- **Concentration is one spell at a time.** Casting a new concentration spell drops the old one.
- **Opportunity attacks use your reaction.** One per round, not per turn.
- **Sneak Attack is once per turn, not once per round.** A Rogue can Sneak Attack on an opportunity attack (different turn).
- **Saving throw proficiency comes from class, not ability score.** Not everyone proficient in DEX skills is proficient in DEX saves.

### Narrative Pitfalls
- **Don't play the characters for the players.** Describe the situation, let them decide.
- **Don't always have the right answer available.** Some situations should be ambiguous.
- **Don't negate player choices.** If they found a creative solution, let it work (or partially work).
- **Don't metagame as DM.** Monsters don't know a player's AC or HP. Play them with the information they'd realistically have.
- **Don't railroad.** Provide hooks and consequences, but let players go off-script.

### Pacing Pitfalls
- **Don't describe everything.** Focus on what's interesting or relevant.
- **Don't let combat drag.** If a fight is clearly won, narrate the mop-up and move on.
- **Don't front-load exposition.** Reveal lore through play, not monologues.

---

## Handling Edge Cases

When a situation isn't clearly covered by the rules:

1. **Check these docs first.** The answer is probably here.
2. **Apply the closest rule.** If a player wants to throw sand in an enemy's eyes, treat it like an improvised attack that might cause the Blinded condition (DC based on the attacker's Athletics or Sleight of Hand vs. target's AC or DEX save).
3. **Use the DC table.** If you can't find a specific rule, set an appropriate DC from the table in `01_CORE_MECHANICS.md` and let them roll.
4. **Rule in the player's favor for cool ideas.** If it's creative and plausible, err on the side of "yes, and roll for it."
5. **Be consistent.** Track your rulings so the same situation gets the same treatment next time.

---

## Session Start Checklist

Before starting a session, verify:
- [ ] Campaign state is loaded (quest log, NPC relationships, party status)
- [ ] Current session plan is referenced (if prepared)
- [ ] Party composition is known (classes, levels, AC, HP, key features)
- [ ] Relevant monster stat blocks are accessible
- [ ] Any ongoing effects are tracked (curses, conditions, quest timers)

## Session End Checklist

After each session, update:
- [ ] Party HP, spell slots, and resources spent
- [ ] XP awarded (if tracking)
- [ ] Loot distributed
- [ ] Quest log updated
- [ ] NPC relationships modified based on actions
- [ ] World state changes logged
- [ ] Notes on unresolved threads for next session
