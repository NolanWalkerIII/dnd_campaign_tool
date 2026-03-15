# Conditions Reference

Conditions alter a creature's capabilities. Applied by spells, class features, monster abilities, and environmental effects. A condition lasts until it's countered by a specified method or for the duration specified by the effect that imposed it.

Multiple conditions can apply simultaneously. If contradictory, apply all of them (e.g., a creature can be prone and restrained at the same time).

---

## Blinded
- Can't see. Auto-fail any check that requires sight.
- Attack rolls against the creature have **advantage**.
- The creature's attack rolls have **disadvantage**.

*Common sources*: Blindness/Deafness spell, Color Spray, darkness effects, some monster abilities.

---

## Charmed
- Can't attack the charmer or target them with harmful abilities or spells.
- The charmer has **advantage** on social interaction checks (CHA) against the creature.

*Does not*: Force the creature to obey commands (unless the specific spell/ability says so — Dominate Person does, Charm Person doesn't).

*Common sources*: Charm Person, Hypnotic Pattern, vampire charm, some fey abilities.

---

## Deafened
- Can't hear. Auto-fail any check that requires hearing.

*Mechanical impact is limited.* Mostly matters for Perception checks, communication, and spells with verbal components (a deafened caster can still cast spells with V components — they just can't hear themselves).

*Common sources*: Blindness/Deafness spell, Thunderwave (sometimes houserule), some monster abilities.

---

## Exhaustion
Cumulative condition with 6 levels. Multiple effects stack.

| Level | Effect |
|-------|--------|
| 1 | Disadvantage on ability checks |
| 2 | Speed halved |
| 3 | Disadvantage on attack rolls and saving throws |
| 4 | Hit point maximum halved |
| 5 | Speed reduced to 0 |
| 6 | Death |

Effects are cumulative. A creature at exhaustion level 3 has disadvantage on ability checks, half speed, and disadvantage on attacks and saves.

**Gaining exhaustion**: Forced march (CON save each hour past 8), starvation, extreme temperatures, Berserker Barbarian's Frenzy, Sickening Radiance spell, some monster abilities.

**Removing exhaustion**: One level removed per long rest (with food and drink). Greater Restoration removes one level. The only way to remove exhaustion faster than one-per-rest without magic.

This is one of the nastiest conditions in the game because of how hard it stacks and how slowly it clears.

---

## Frightened
- **Disadvantage** on ability checks and attack rolls while the source of fear is in line of sight.
- Can't willingly move closer to the source.

*Common sources*: Cause Fear, Fear spell, Frightful Presence (dragons), Turn Undead, Wrathful Smite, some monster abilities.

---

## Grappled
- Speed becomes **0**. Can't benefit from any bonus to speed.
- Ends if the grappler is incapacitated or if the target is moved out of reach.

*Does not*: Impose disadvantage on attacks, restrain, or prevent spellcasting.

See `05_COMBAT.md` for grapple rules.

---

## Incapacitated
- Can't take **actions** or **reactions**.

*Does not*: Prevent movement or bonus actions (technically). But most sources that cause incapacitation also prevent movement (stunned, unconscious, etc.).

---

## Invisible
- Impossible to see without magic or special sense. For hiding purposes, heavily obscured. Location can still be detected by noise, tracks, etc.
- Attack rolls against the creature have **disadvantage**.
- The creature's attack rolls have **advantage**.

*Common sources*: Invisibility, Greater Invisibility, certain class features (Arcane Trickster's Magical Ambush, Gloom Stalker in darkness).

Attacking or casting a spell that targets a creature reveals your location (even if you remain invisible from Greater Invisibility).

---

## Paralyzed
- **Incapacitated**. Can't move or speak.
- Auto-fail STR and DEX saving throws.
- Attack rolls against have **advantage**.
- Any attack that hits from within **5 feet** is a **critical hit**.

This is devastating. Hold Person/Hold Monster are encounter-ending spells if the target fails.

*Common sources*: Hold Person, Hold Monster, ghoul's Claws, some poisons.

---

## Petrified
- Transformed to solid inanimate substance (usually stone). Weight × 10.
- **Incapacitated**. Can't move or speak. Unaware of surroundings.
- Auto-fail STR and DEX saving throws.
- Attack rolls against have **advantage**.
- **Resistance** to all damage.
- Immune to poison and disease (existing ones suspended, not removed).
- Does not age.

*Common sources*: Flesh to Stone, basilisk gaze, medusa gaze, cockatrice bite.

*Removal*: Greater Restoration, Wish, specific conditions stated in the effect.

---

## Poisoned
- **Disadvantage** on attack rolls and ability checks.

Simple but impactful. Very common condition — lots of monsters and traps inflict it.

*Common sources*: Poison damage effects, Ray of Sickness, Contagion, spider bites, assassin poisons, many monster attacks.

---

## Prone
- Can only crawl (1 extra foot per foot moved). Must spend **half movement** to stand up.
- **Disadvantage** on attack rolls.
- Melee attacks within 5 ft against the creature have **advantage**.
- Ranged attacks against the creature have **disadvantage**.

*Common sources*: Shove action, spells (Grease, Sleet Storm, Tasha's Hideous Laughter), tripping, some monster abilities.

Dropping prone is free and costs no movement — useful to get the ranged disadvantage as a defensive move.

---

## Restrained
- Speed becomes **0**. Can't benefit from any bonus to speed.
- Attack rolls against have **advantage**.
- The creature's attack rolls have **disadvantage**.
- **Disadvantage** on DEX saving throws.

Strictly worse than grappled (which only sets speed to 0).

*Common sources*: Entangle, Web, grappler feat pin, net, some monster abilities (giant spider, roper).

---

## Stunned
- **Incapacitated**. Can't move. Can speak only falteringly.
- Auto-fail STR and DEX saving throws.
- Attack rolls against have **advantage**.

Like a slightly less extreme paralyzed (no auto-crits from melee).

*Common sources*: Stunning Strike (Monk), Power Word Stun, Divine Word, some monster abilities.

---

## Unconscious
- **Incapacitated**. Can't move or speak. Unaware of surroundings.
- Drops whatever it's holding and falls **prone**.
- Auto-fail STR and DEX saving throws.
- Attack rolls against have **advantage**.
- Attacks from within 5 ft are **critical hits**.

*Common sources*: Dropping to 0 HP, Sleep spell, being knocked out (attacker can choose nonlethal on the killing blow with melee), some poisons.

---

## Condition Interaction Quick Reference

| Condition | Disadvantage on Attacks | Advantage on Attacks vs. | Speed 0 | Auto-fail STR/DEX Saves |
|-----------|------------------------|--------------------------|---------|------------------------|
| Blinded | Yes | Yes | No | No |
| Charmed | No (can't attack charmer) | No | No | No |
| Frightened | Yes (if source visible) | No | No | No |
| Grappled | No | No | Yes | No |
| Invisible | No (has advantage) | Yes (disadvantage vs.) | No | No |
| Paralyzed | Can't attack | Yes + auto-crit in 5ft | Can't move | Yes |
| Petrified | Can't attack | Yes | Can't move | Yes |
| Poisoned | Yes | No | No | No |
| Prone | Yes | Melee: Yes / Ranged: No (disadvantage) | No (crawl) | No |
| Restrained | Yes | Yes | Yes | No (disadvantage DEX saves) |
| Stunned | Can't act | Yes | Can't move | Yes |
| Unconscious | Can't act | Yes + auto-crit in 5ft | Can't move (prone) | Yes |
