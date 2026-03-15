# Dungeon Master Guide

Rules and guidance for running a 5e game. This is the operational reference for an LLM acting as DM.

## The DM's Job

Three core responsibilities:

1. **Describe the world** — what the players see, hear, smell, feel.
2. **Adjudicate rules** — determine what happens when players act. Call for rolls, set DCs, apply outcomes.
3. **Control NPCs and monsters** — play every character that isn't a player character. Give them goals, personality, and tactical behavior.

---

## Encounter Building

### XP Budget Method (DMG)

For a party of 4 characters, calculate XP thresholds:


| Difficulty | XP per Character (by Level) |
| ---------- | --------------------------- |
|            | Lv1                         |
| Easy       | 25                          |
| Medium     | 50                          |
| Hard       | 75                          |
| Deadly     | 100                         |



|        | Lv11  | Lv12  | Lv13  | Lv14  | Lv15  | Lv16  | Lv17  | Lv18  | Lv19   | Lv20   |
| ------ | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ------ | ------ |
| Easy   | 800   | 1,000 | 1,100 | 1,250 | 1,400 | 1,600 | 2,000 | 2,100 | 2,400  | 2,800  |
| Medium | 1,600 | 2,000 | 2,200 | 2,500 | 2,800 | 3,200 | 3,900 | 4,200 | 4,900  | 5,700  |
| Hard   | 2,400 | 3,000 | 3,400 | 3,800 | 4,300 | 4,800 | 5,900 | 6,300 | 7,300  | 8,500  |
| Deadly | 3,600 | 4,500 | 5,100 | 5,700 | 6,400 | 7,200 | 8,800 | 9,500 | 10,900 | 12,700 |


**Process:**

1. Multiply the per-character XP by number of characters to get party threshold.
2. Add up XP values of all monsters in the encounter.
3. Apply the multiplier for number of monsters (see `11_MONSTER_GUIDE.md`).
4. Compare adjusted XP to party thresholds.

### Quick Encounter Guidelines

For a party of 4 at level X, a single monster of CR X is a medium encounter. Use these rules of thumb:

- **Easy**: CR = party level - 2 (or 2-3 weak monsters)
- **Medium**: CR = party level (or 4-5 moderate monsters)
- **Hard**: CR = party level + 2 (or a mix of strong + weak)
- **Deadly**: CR = party level + 3-4 (risk of character death)
- **Boss fight**: One creature CR = party level + 3, with 2-4 minions at CR 1/4 to 1

### Adventuring Day XP Budget

The game is balanced around ~6-8 medium encounters per long rest, with 2 short rests mixed in. Most tables don't run this many encounters. If you run fewer encounters per day, each encounter should be harder to challenge the party — they'll have more resources per fight.


| Level | Daily XP Budget (per character) |
| ----- | ------------------------------- |
| 1     | 300                             |
| 2     | 600                             |
| 3     | 1,200                           |
| 4     | 1,700                           |
| 5     | 3,500                           |
| 6     | 4,000                           |
| 7     | 5,000                           |
| 8     | 6,000                           |
| 9     | 7,500                           |
| 10    | 9,000                           |
| 11-20 | (continues scaling)             |


---

## Setting Difficulty Classes

### The DC Table


| Task              | DC  |
| ----------------- | --- |
| Trivial           | 5   |
| Easy              | 10  |
| Moderate          | 15  |
| Hard              | 20  |
| Very Hard         | 25  |
| Nearly Impossible | 30  |


### When to Call for a Roll

Roll when:

- There's a meaningful chance of failure
- Failure has interesting consequences
- The task isn't trivially easy or impossible

Don't roll when:

- Success is guaranteed (proficient character doing something routine)
- Failure would halt the story with no alternatives
- The attempt is impossible regardless of roll

### Degrees of Success (Optional)

Failure by 5+ can mean a worse outcome. Success by 5+ can mean a bonus result. This isn't RAW but most experienced DMs use it.

---

## Running NPCs

### NPC Quick Creation

Give each NPC exactly 3 things:

1. **Appearance detail**: One visual thing the players notice first.
2. **Mannerism**: How they talk or move (nervous twitch, speaks in rhymes, laughs before every sentence).
3. **Goal**: What they want right now. This drives their behavior.

That's enough to roleplay convincingly. You don't need a backstory for every shopkeeper.

### NPC Attitudes


| Attitude    | Behavior                            | DC to Shift                          |
| ----------- | ----------------------------------- | ------------------------------------ |
| Hostile     | Works against the party, may attack | DC 20 Persuasion to make Indifferent |
| Indifferent | Doesn't care, minimal help          | DC 15 to make Friendly               |
| Friendly    | Willing to help, shares info        | Already cooperative                  |


### Social Interaction Rules

Don't reduce all social encounters to single Persuasion rolls. Use this structure:

1. What does the NPC want?
2. What would convince them?
3. Does the player's approach address their motivations?

Rolls modify the outcome, not replace the conversation. A good argument with a mediocre roll should still get partial results. A terrible argument with a nat 20 shouldn't work miracles — Persuasion isn't mind control.

---

## Awarding Experience

### XP Method

Divide total monster XP equally among surviving party members. Non-combat encounters should also award XP — traps solved, social encounters resolved, objectives completed. Use monster-equivalent XP for these (a hard negotiation might be worth a medium encounter's XP).

### Milestone Method

Party levels up when they complete significant story objectives. No XP tracking. More narrative-driven. The DM decides when the party has earned a level. Most common approach in modern 5e play.

### Mixed Approach

Award XP for combats and milestones for story beats. Some tables like this hybrid.

---

## Treasure and Rewards

### Treasure by CR


| CR    | Individual Treasure              | Hoard Treasure                                                     |
| ----- | -------------------------------- | ------------------------------------------------------------------ |
| 0-4   | 1-10 gp, maybe a gem             | 200-600 gp + 1d6 mundane items + 0-2 uncommon magic items          |
| 5-10  | 10-100 gp, possibly a gem or art | 1,000-6,000 gp + art objects + 1d4 uncommon + 0-1 rare magic items |
| 11-16 | 100-1,000 gp + potential magic   | 10,000-50,000 gp + rare and very rare items                        |
| 17+   | 1,000+ gp + potential magic      | 50,000+ gp + very rare and legendary items                         |


These are rough guidelines from the DMG random treasure tables. Adjust to fit your campaign.

### Magic Item Distribution Guidance


| Tier | Levels | Typical Items                                                  |
| ---- | ------ | -------------------------------------------------------------- |
| 1    | 1-4    | Common and uncommon. +1 weapons/armor are exciting finds.      |
| 2    | 5-10   | Uncommon and rare. +1 items are standard, +2 starts appearing. |
| 3    | 11-16  | Rare and very rare. +2 standard, +3 rare finds.                |
| 4    | 17-20  | Very rare and legendary. Artifacts in play.                    |


---

## Running Combat (DM Tips)

### Monster Tactics

Not every monster fights to the death. Consider:

- **Intelligent monsters** retreat, set ambushes, use terrain, call for reinforcements.
- **Animals** flee at half HP unless defending young or cornered.
- **Undead and constructs** typically fight until destroyed (no self-preservation).
- **Pack creatures** focus fire on wounded targets. Wolves knock prone and let allies attack with advantage.
- **Spellcasters** stay at range, use cover, counterspell key player spells, buff allies.

### Initiative and Turn Order Tips

- Group identical monsters on one initiative to speed play.
- Have monster actions pre-planned for the first round.
- Track HP visibly (for yourself) — use a table or list.

### Describing Combat

Don't just say "the goblin hits you for 7 damage." Describe the action:

- "The goblin lunges with its scimitar, catching you across the forearm. Take 7 slashing damage."
- On a miss: "The arrow whistles past your ear, embedding in the wall behind you."
- On a kill: Let the player describe how they finish the enemy.

---

## Rulings Over Rules

The DM's most important power: making rulings when the rules don't cover a situation. Principles:

1. **Say yes or roll for it.** If the player's idea is reasonable, either let it work or set a DC.
2. **If it makes sense, it works.** Don't block creative solutions because there isn't a specific rule.
3. **Be consistent.** If you rule that a chandelier can be swung on for advantage, that should work next time too.
4. **Keep the game moving.** If you can't find a rule in 30 seconds, make a ruling and look it up later.

---

## Random Tables (DM Tools)

### Random NPC Traits

**Personality (d10):**

1. Paranoid — trusts no one
2. Cheerful — optimistic even in danger
3. Gruff — few words, direct
4. Scholarly — quotes books constantly
5. Nervous — fidgets, stutters
6. Devout — references their god frequently
7. Greedy — everything has a price
8. Melancholic — speaks of past loss
9. Boastful — exaggerates everything
10. Mysterious — gives cryptic answers

**Motivation (d8):**

1. Gold
2. Revenge
3. Protect someone
4. Find a lost item
5. Escape a pursuer
6. Gain power
7. Uncover a secret
8. Repay a debt

### Random Encounter Complications (d6)

1. Weather changes suddenly (storm, fog)
2. A third party arrives (reinforcements, bystanders, rival adventurers)
3. The terrain shifts (bridge collapses, cave-in, flood)
4. A monster flees and leads to something worse
5. An NPC ally gets in the way or needs protection
6. One monster is actually an illusion / shapechanger / under a curse

### Quick Dungeon Room Contents (d10)

1. Empty (but has clue)
2. Monster (guard patrol)
3. Monster + treasure
4. Trap
5. Trap + treasure
6. Puzzle / skill challenge
7. NPC (prisoner, merchant, quest giver)
8. Environmental hazard
9. Hidden treasure (requires investigation)
10. Boss or mini-boss encounter

---

## Session Structure

### Session Zero (Before the Campaign)

Establish:

- Campaign tone and themes
- PC creation (together, so characters fit the party)
- House rules
- Content limits and safety tools
- How death and resurrection work in this campaign
- Expected game schedule and session length

### Typical Session Flow

1. **Recap** (2-5 min): What happened last time.
2. **Pickup**: Resume where you left off. Address any cliffhangers.
3. **Exploration / RP** (30-60 min): Travel, investigation, NPC interaction, puzzle-solving.
4. **Combat** (30-60 min): 1-3 encounters per session is typical.
5. **Wrap-up** (5-10 min): Resolve the session's arc, set up the next hook.

### Pacing

- If players are stuck, give them a clue (an NPC hints at a solution, they find a note, etc.).
- If combat is dragging, reduce remaining monster HP or have them retreat.
- If RP is wandering, introduce a time pressure or event.
- End on a hook — a revelation, a cliffhanger, or a new quest.

