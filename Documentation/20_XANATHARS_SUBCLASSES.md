# Xanathar's Guide to Everything — Subclasses Reference

All subclasses from XGtE. Organized by class (alphabetical). Each includes feature progression with mechanics, numbers, and action economy. No flavor — pure reference material for LLM use.

---

## Barbarian

**Subclass gained at Level 3 (Primal Path)**

### Path of the Ancestral Guardian

**Level 3 — Ancestral Protectors**
- Reaction when you rage and a creature within 5 ft makes an attack roll against another creature, you can use your reaction to interfere. The attacker has disadvantage on the roll. If it hits anyway, it deals no extra damage from critical hits.
- Reaction is per attacker per turn, triggers when rage starts and whenever you use Ancestral Protectors.

**Level 6 — Spirit Shield**
- Reaction when you or a creature within 30 ft takes damage, you can use your reaction to reduce damage by 2d6 + WIS modifier.
- Once used, you can't use this again until the start of your next turn.

**Level 10 — Consult the Spirits**
- Advantage on WIS (Insight) and WIS (Perception) checks.
- Can cast *augury* or *clairvoyance* using your action, no material cost, can't use this ability again until a short or long rest.

**Level 14 — Vengeful Ancestors**
- Reaction when a creature within 30 ft attacks a creature other than you, you can use your reaction to make a melee weapon attack against the attacker. You can move up to half your speed as part of this reaction.

**Mechanical notes**: Guardian Barbarian trades damage scaling for party protection. Ancestral Protectors is reactive damage mitigation, stackable per attack (not per turn). Spirit Shield burns your reaction but is repeatable per turn. At high levels you become a mobile counter-attacker.

---

### Path of the Storm Herald

**Level 3 — Storm Aura**
- Choose a damage type: cold, lightning, or thunder.
- At the start of each turn, you can activate the aura until the end of the turn. Each creature within 10 ft makes a save against your spell DC (8 + proficiency + CON mod). On fail, takes damage equal to 2d6 (scales: d6 at 3, d6 at 5, d6 at 7, etc., reaching 3d6 at 14+).
- At level 5, creatures have disadvantage on the save.
- Damage type is chosen at subclass selection, not changeable.

**Level 6 — Storm Soul**
- Resistance to the damage type of your aura.
- Gain 1 additional use of Rage per long rest.

**Level 10 — Shielding Storm**
- When a creature within 10 ft attacks you and you take damage, you can use your reaction to reduce damage by 1d6 + your monk level. When the attacker is within 5 ft, they take damage equal to half the damage reduced.
- Once per turn.

**Level 14 — Raging Storm**
- Whenever you activate the aura on your turn, one creature of your choice within 10 ft takes the aura damage immediately (no save, forced damage).
- All affected creatures within 10 ft also take the damage.

**Mechanical notes**: Storm Herald is AoE-focused damage with scaling difficulty (no scaling save DC is a problem). Aura must be reactivated each turn (action economy tax). Shielding Storm turns damage into deterrent. Raging Storm guarantees some damage but redundantly applies to already-triggered creatures. Damage output is front-loaded; later levels don't add numerical scaling.

---

### Path of the Zealot

**Level 3 — Divine Fury**
- When you hit with a melee weapon attack while raging, add 1d6 extra damage (cold, lightning, or radiant, chosen when you pick subclass). Damage scales to 1d6 at level 3, 1d8 at 10, 1d10 at 14.
- Damage type is locked at subclass selection.

**Level 6 — Warrior of the Gods**
- While raging, your weapon attacks hit targets 10 ft farther away. No penalty for melee attacks at long range.
- No extra die roll or AC adjustment — just extended reach.

**Level 10 — Fanatical Focus**
- When a creature within 30 ft casts a spell that forces you to make a save while you're raging, you can use your reaction to force that creature to make a WIS save (spell DC). On fail, the spell fails.
- Once per rage.

**Level 14 — Zealous Transcendence**
- When you drop to 0 HP while raging, you can use your reaction to instead regain HP = 1d12 + CON mod. You drop to 1 HP if the healing is less.
- Costs 1 Zealot point from your Zealot use pool (shares Rage pool).

**Mechanical notes**: Zealot is pure damage output (guaranteed hit damage, no save needed). Divine Fury is the subclass identity — consistent bonus damage while raging. Fanatical Focus is spell negation once per rage (powerful for counterspell-heavy campaigns). Zealous Transcendence is essentially a pseudo-death-save but consumes Rage uses, making it a resource trade-off.

---

## Bard

**Subclass gained at Level 3 (Bard College)**

### College of Glamour

**Level 3 — Mantle of Inspiration**
- Reaction when a creature you can see within 60 ft makes an ability check, attack roll, or saving throw, you can use your reaction to grant them a Bardic Inspiration die (rolling it) as a bonus to the roll. They gain the benefit after seeing the roll but before the outcome is determined.
- No uses limited by uses per day — functions once per attack/check/save you witness.
- Inspiration die = Bardic Inspiration die (d6 baseline, scales normally).

**Level 6 — Enthralling Performance**
- When you perform with music, instrument, or speech within 60 ft, creatures of your choice that can hear and see you must make a CHA save (spell DC) or be charmed for 1 minute.
- You can target a number of creatures = 1 + CHA modifier.
- They can repeat the save if they or an ally takes damage. Charmed condition ends normally.
- Performance requires 1 minute of uninterrupted performance.

**Level 10 — Unflappable Performer**
- No longer need to make concentration checks when concentrating on spells while performing.
- If you're interrupted during performance, you can restart it as a bonus action on your next turn (no penalty).

**Level 14 — Peerless Skill**
- When you make an ability check, you can roll your Bardic Inspiration die and add the result to your check (before seeing the outcome).
- Once per ability check. Can apply to checks you're not proficient in.

**Mechanical notes**: Glamour is a reaction-based support subclass. Mantle of Inspiration is reactive healing/boost on any roll you witness. Enthralling Performance is a mass charm (1-minute AoE control). The action economy is efficient — most features are reactions or bonus actions. Peerless Skill turns Inspiration into self-buff.

---

### College of Swords

**Level 3 — Bonus Proficiencies**
- Medium armor and scimitars.

**Level 3 — Fighting Style**
- Same as Fighter: Archery (+2 ranged), Defense (+1 AC in armor), Dueling (+2 damage one-handed), Great Weapon Fighting (reroll 1s/2s on damage), or Two-Weapon Fighting (add ability mod to off-hand).

**Level 3 — Blade Flourish**
- When you take the Attack action on your turn, you can replace one of your attacks with a Blade Flourish (melee weapon attack with advantage). On hit, you can spend 1 Bardic Inspiration die to add its damage and pick one flourish effect:
  - **Defensive Flourish**: Add the die to AC until the start of your next turn.
  - **Slashing Flourish**: Spend your movement to move up to your speed without provoking opportunity attacks.
  - **Mobile Flourish**: Make another melee attack as a bonus action.
- Die damage is added to the attack roll damage; effect applies after a hit.

**Level 6 — Extra Attack**
- You can attack twice, instead of once, when you take the Attack action on your turn.

**Level 10 — Master's Flourish**
- You can use Blade Flourish without spending an Inspiration die (but the attack has no advantage and doesn't add die damage). Once per turn.

**Level 14 — Cutting Words** (modified for Swords)
- When a creature within 60 ft makes an attack roll, ability check, or damage roll, you can use your reaction to expend a Bardic Inspiration die and subtract the number rolled from their result.
- If the creature is within 5 ft, it has disadvantage on the attack (or ability check/damage roll is reduced by that amount, not rolled normally).

**Mechanical notes**: Swords is an armor-wearing, melee-focused bard with blade tricks. Blade Flourish provides scaling damage (die + weapon) with tactical options (Defense adds AC, Mobile adds attacks, Slashing conserves movement). Master's Flourish at 10 removes the Inspiration cost but locks you to once per turn. Cutting Words is a reaction debuff, scaled for proximity.

---

### College of Whispers

**Level 3 — Psychic Blades**
- When you hit a creature with a weapon attack within 1 minute of using Bardic Inspiration on a different creature, add your Bardic Inspiration die to the damage (psychic damage).
- Add damage once per turn to a single attack.

**Level 6 — Words of Intrigue**
- When you cast a spell or make a weapon attack within 60 ft, choose a creature you can see and they must make a WIS save (spell DC) or take 3d6 psychic damage.
- Once per long rest, or when you expend a Bardic Inspiration die, this recharges. Feature is deliberately obscure — it's a bonus action divination/mind-read utility, not combat damage.
- Actually grants advantage on Deception and Insight checks, and you can cast *disguise self* and *invisibility* at will, no spell slots.

**Level 10 — Peerless Skill**
- When you make a check to deceive, intimidate, or charm, roll a Bardic Inspiration die and add the result.
- No limit on uses.

**Level 14 — Psychic Scream**
- Reaction when a creature within 60 ft that you can see makes an attack roll, ability check, or saving throw, you can use your reaction to subtract your CHA modifier from their roll (minimum 0).
- Costs 1 use of Bardic Inspiration die roll.

**Mechanical notes**: Whispers is a manipulation-focused assassin bard. Psychic Blades requires setup (inspire someone else first, then attack within 1 minute). Words of Intrigue is a mixed bag — casting *disguise self*/*invisibility* at will is excellent stealth utility. Peerless Skill makes you a social powerhouse. Psychic Scream is a debuff reaction similar to Cutting Words but uses up Inspiration rolls.

---

## Cleric

**Subclass gained at Level 1 (Divine Domain)**

### Forge Domain

**Level 1 — Bonus Proficiencies**
- Heavy armor, martial weapons.
- Smithing's tools proficiency.

**Level 1 — Blessing of the Forge**
- When you finish a long rest, you can imbue a nonmagical weapon or item of armor worn by you with a +1 to attack rolls (weapons) or AC (armor). This bonus lasts until the next long rest.
- Only one item can benefit at a time.
- You're considered proficient in any armor.

**Level 2 — Channel Divinity: Artisan's Blessing**
- Action to touch a nonmagical object and repair it as if you spent 1 hour working on it. If the object is completely destroyed, you can't repair it.
- Unlimited uses when you have Channel Divinity (2 per short rest at level 6).

**Level 6 — Soul of the Forge**
- Resistance to fire damage.
- When you wear heavy armor, you gain a bonus to AC = 1 (stacks with Blessing of the Forge).

**Level 8 — Divine Strike**
- When you hit with a melee weapon attack, add 1d8 fire damage (1d6 at level 8, scaling to 1d8 at 11, 1d10 at 14, 1d12 at 17).

**Level 17 — Anvil of Souls**
- You add your WIS modifier to the AC bonus provided by Blessing of the Forge.
- If you're wearing heavy armor, you gain half your WIS modifier (rounded down) to damage rolls on melee weapons using STR/DEX.

**Mechanical notes**: Forge Cleric is a tank/support hybrid. Blessing grants a passive +1 to one item per day (not stacking, mandatory choice). Soul of the Forge adds +1 AC in heavy armor (net +2 from medium baseline). Divine Strike adds fire damage to attacks. At level 17, WIS scaling is added to AC. Artisan's Blessing is utility for object repair.

---

### Grave Domain

**Level 1 — Bonus Proficiencies**
- Martial weapons, heavy armor.

**Level 1 — Circle of Mortality**
- You learn the *spare the dying* cantrip. When you cast it, the target regains 1 HP instead of stabilizing (at no cost, action or otherwise).
- You can cast it at 30 ft range (normal range is touch).
- When you cast a spell to restore HP to a creature at 0 HP, they roll a d4 and add it to the healing (bonus healing, not doubled).

**Level 2 — Channel Divinity: Path to the Grave**
- Action to touch a creature and curse it for 1 minute. The next attack roll against the cursed creature within 1 minute has advantage, and if hit, ignores resistance and immunity to the damage type. Curse ends if the creature is hit or the spell ends.
- Unlimited uses when you have Channel Divinity (2 per short rest at level 6).

**Level 6 — Sentinel at Death's Door**
- Reaction when you or an ally within 30 ft takes damage, you can use your reaction to reduce the damage by 1d8 + your WIS modifier.
- Once per turn.

**Level 8 — Divine Strike**
- When you hit with a melee weapon attack, add 1d8 necrotic damage (scales: d6 at 8, d8 at 11, d10 at 14, d12 at 17).

**Level 17 — Keeper of Souls**
- Reaction when a creature you can see within 30 ft drops to 0 HP, you can use your reaction to let that creature regain 1 HP instead.
- Once per long rest.

**Mechanical notes**: Grave Cleric is burst-damage support with death prevention. Circle of Mortality is free at-will healing cantrip (at range, bonus 1 HP to down targets). Path to the Grave is setup for allies — grants advantage and pierces resistance for the next hit within 1 minute (powerful for crit-fishing). Sentinel reduces damage preemptively (1d8 + WIS per turn). Divine Strike adds necrotic damage. Keeper of Souls is a once-per-long-rest save-from-death (no resource cost).

---

## Druid

**Subclass gained at Level 2 (Druid Circle)**

### Circle of Dreams

**Level 2 — Balm of the Summer Court**
- Whenever you finish a short or long rest, you can choose yourself and a number of allies = your WIS modifier (minimum 1). Each gains temporary HP = your Druid level + WIS modifier.
- Stacks with other temp HP sources (doesn't override, adds).

**Level 2 — Hearth of Moonlight and Shadow**
- When you finish a long rest, you can create a small hut in a space within 5 ft. It lasts until the next long rest or when you dismiss it (action).
- The hut is 15 ft in diameter, can fit up to 9 creatures (you choose), no one can leave without your consent (magical barrier prevents exit for hostile intent). All creatures inside gain +2 AC and +2 to saves while in the hut.
- No saves needed; you control the hut completely.

**Level 6 — Therapeutic Aura**
- When a creature within 15 ft of you makes a save or ability check, they add your WIS modifier to the roll.
- Applies to all creatures, not just allies (no limit on when you can use this).

**Level 10 — Dream Reflection**
- When a creature within 5 ft that you can see casts a spell and you're aware of it, you can use your reaction to add your WIS modifier to their spell's saving throw DC (if it has one).
- Once per turn.

**Level 14 — One with the Wild**
- While you have at least 1 HP and you're in contact with the ground, you gain the following benefits:
  - You don't need to sleep (Balm still recharges as normal from rests).
  - You have advantage on WIS (Perception) checks.
  - You can move through nonmagical difficult terrain without expending extra movement.
  - Creatures you choose within 5 ft gain half those benefits (except movement).

**Mechanical notes**: Dreams is a healing/buffing support circle. Balm grants temp HP to up to WIS mod allies after each rest (significant at higher WIS). Hearth is a long-rest-duration zone providing +2 AC and saves to 9 creatures. Therapeutic Aura is a passive ability check/save buff (+WIS mod). Dream Reflection boosts spell DCs reactively. One with the Wild is mobility and perception enhancement at 14.

---

### Circle of the Shepherd

**Level 2 — Speech of the Woods**
- You can communicate with beasts (not humanoids with animal features, actual beasts). Beasts understand your words (Insight checks to determine if they're helpful).
- When beasts see you, they are indifferent to you (no hostility unless provoked).

**Level 2 — Spirit Totem**
- Bonus action to create a spirit totem in a space within 30 ft that you can see. Totem lasts 1 minute and can be summoned again on a short rest.
- Choose a totem form:
  - **Unicorn Totem**: Creatures within 30 ft that you can see gain temporary HP = your Druid level when they join the combat (once when they join, not per turn).
  - **Bear Totem**: Creatures within 30 ft gain advantage on melee weapon attacks and saving throws vs. fear.
  - **Hawk Totem**: Creatures within 30 ft get opportunity attacks when a creature moves away from them (bonus action, not your action).
- You can maintain up to 1 totem at a time (you choose which, can replace on your turn).
- Using the totem's effect requires no action from you (automatic aura).

**Level 6 — Mighty Summoner**
- Beasts summoned by your spells gain hit points = your Druid level (bonus HP, added to their normal maximum).
- When you cast *conjure animals*, you can choose the specific creatures instead of random rolls.

**Level 10 — Guardian Spirit**
- When a creature within 30 ft of your spirit totem drops to 0 HP, you can use your reaction (no action cost) to restore 1d4 + your Druid level HP to that creature.
- Once per long rest.

**Level 14 — Faithless Totem**
- You can summon a second spirit totem, maintaining both (up to 2 now).
- When a creature within 30 ft of one of your totems makes a save, they add 1d4 to the save (no limit on uses).

**Mechanical notes**: Shepherd is a summoner/support circle. Speech of the Woods is beast communication utility. Spirit Totem is a placed aura (30 ft) with three switchable effects — Unicorn grants temp HP to new combatants, Bear buffs attacks/saves, Hawk enables bonus opportunity attacks. Mighty Summoner upgrades conjured animals (more HP, choice of creatures). Guardian Spirit is emergency healing from the totem location once per long rest. Faithless Totem allows 2 totems at once and grants save boosts.

---

## Fighter

**Subclass gained at Level 3 (Martial Archetype)**

### Arcane Archer

**Level 3 — Arcane Archer Lore**
- You learn two wizard cantrips of your choice (from the Wizard spell list). These are spellcasting, using INT as your spellcasting ability.

**Level 3 — Arcane Shot**
- When you hit with a ranged weapon attack, you can expend one Arcane Shot die (d4, scaling to d6 at 7, d8 at 15, d10 at 18) to add one Arcane Shot option. You know 2 options initially (3 at 7, 4 at 15, 5 at 18).
- Options include:
  - **Bonus Damage**: Add the die to the damage roll.
  - **Force Blast**: Target makes STR save (spell DC = 8 + proficiency + DEX mod). On fail, pushed back 5 ft and knocked prone.
  - **Mystical Shot**: Target makes WIS save. On fail, disadvantage on next attack roll before the end of your next turn.
  - **Piercing Shot**: The arrow ignores cover.
- Uses = 2 per short rest at level 3 (4 at 7, 5 at 15, 6 at 18).
- You regain 1 use when you finish a short or long rest (minimum 1).

**Level 7 — Extra Attack**
- Attack twice, instead of once, when you take the Attack action on your turn.

**Level 7 — Ever-Ready Arcane Aura**
- Whenever you finish a short or long rest, one weapon of your choice gains an arcane aura until the next rest. When you hit with that weapon, add your INT modifier to the damage roll (minimum 1).
- Non-magical weapons become magical while enchanted.

**Level 15 — Improved Arcane Shot**
- You can use Arcane Shot twice per attack (up to 2 die expenditures per arrow). You can apply the same effect twice or different options to the same attack.

**Level 18 — Masterwork Ammunition**
- Your ranged weapon attacks ignore nonmagical resistance and immunity to damage (treats resistances as normal damage, immunity as resistance).

**Mechanical notes**: Arcane Archer is a ranged utility fighter. Arcane Shot uses d4-d10 dice with flexible effects (damage, control, debuff). Uses recharge on short rest. Ever-Ready Aura adds INT to damage rolls on one weapon. Improved Arcane Shot allows 2 dice per attack. Masterwork Ammunition pierces resistances. Lore grants cantrips for utility out-of-combat.

---

### Cavalier

**Level 3 — Bonus Proficiencies**
- All armor, all simple and martial melee weapons.

**Level 3 — Fighting Style**
- Choose one: Archery (+2 ranged), Defense (+1 AC in armor), Dueling (+2 damage one-handed), Great Weapon Fighting (reroll 1s/2s on damage), Protection (impose disadvantage on attack against adjacent ally with shield), or Two-Weapon Fighting (add ability mod to off-hand).

**Level 3 — Born to the Saddle**
- Advantage on saves to avoid being knocked prone while mounted.
- If a mount is knocked prone, you can use your reaction to dismount as the mount falls and land on your feet.
- Mounting and dismounting costs 5 ft movement (instead of half movement).

**Level 3 — Unwavering Mark**
- Whenever a creature within 5 ft makes an attack roll against a target other than you, you can use your reaction to make a melee weapon attack against the attacker (if you can reach them).
- Once per attack.

**Level 7 — Warding Maneuver**
- Reaction when you or a creature within 5 ft takes damage, you can roll a d8 and subtract the number from the damage (minimum 0).
- Uses = 1 + CON modifier per short rest (minimum 1).

**Level 10 — Extra Attack**
- Attack twice, instead of once, when you take the Attack action on your turn.

**Level 15 — Defender of the Realm**
- Whenever a creature within 5 ft makes an attack roll, you can use your reaction to make a melee weapon attack against that creature. You move up to half your speed as part of this reaction (doesn't reduce your speed on your turn).
- Once per turn.

**Level 18 — Undying Sentinel**
- Once per turn, you can subtract 1d4 from your own attack roll, ability check, or saving throw after seeing the result but before any effects resolve. Roll the d4 and subtract (damage reduction, not granted bonus).

**Mechanical notes**: Cavalier is a mounted tank/interrupter. Born to the Saddle is mount utility. Unwavering Mark and Defender of the Realm are reaction attacks when enemies target allies. Warding Maneuver is a damage-reducing reaction (d8 + CON uses per rest). Extra Attack at 10. Undying Sentinel allows taking-back rolls once per turn (retroactive damage reduction).

---

### Samurai

**Level 3 — Bonus Proficiencies**
- All armor, all simple and martial melee weapons.

**Level 3 — Fighting Style**
- Same as Cavalier/Fighter.

**Level 3 — Warrior's Resolve**
- When you finish a short or long rest, you gain temporary HP = 5 + your Fighter level + your WIS modifier.

**Level 3 — Way of the Warrior** (not the monk subclass)
- You gain a number of ki points = your WIS modifier (minimum 1). You regain all spent ki on a short rest.
- Spend 1 ki to gain advantage on a weapon attack roll on your turn (must decide before rolling).
- When a creature attacks you and you can see the attacker, spend 1 ki as a reaction to gain advantage on the melee attack roll triggered by Unwavering Mark (if you have that).

**Level 7 — Elegant Courtier**
- Advantage on CHA (Persuasion) checks and Insight checks.
- No penalty for not knowing a language (you can always attempt to communicate with creatures you share a language with).

**Level 10 — Extra Attack**
- Attack twice, instead of once, when you take the Attack action on your turn.

**Level 15 — Strength Before Death**
- Reaction when you take damage while you have at least 1 HP, you can expend a ki point to reduce the damage by 1d12 + your WIS modifier.
- Once per long rest without using ki (you can spend 1 ki to use it again).

**Level 18 — Master of Arms**
- You've mastered a fighting style. Choose one Fighting Style option. You can switch the Fighting Style you chose at level 3 to a different option, and gain the benefits of that option instead (all current benefits).
- You can switch once per long rest.

**Mechanical notes**: Samurai is a WIS-based fighter with ki resource. Warrior's Resolve grants temp HP on rest. Way of the Warrior grants ki points = WIS mod, enabling advantage on attacks or reactions. Elegant Courtier is social bonuses. Strength Before Death is a damage reduction reaction (1d12 + WIS per ki spend). Master of Arms allows switching Fighting Styles.

---

## Monk

**Subclass gained at Level 3 (Monastic Tradition)**

### Way of the Drunken Master

**Level 3 — Bonus Proficiencies**
- Martial arts with unarmed strikes and monk weapons.

**Level 3 — Drunken Technique**
- When you use Flurry of Blows, you gain the following benefits until the end of your turn:
  - Your AC = 10 + DEX + WIS + number of ki points you spent (up to +2 if you spent 1-2 ki).
  - When a creature makes an attack roll against you, you have advantage on the save.
  - When you use step of the wind, you gain 10 ft extra movement (scales with level).

**Level 6 — Tipsy Sway**
- When a creature within 5 ft makes an attack roll against you and you can see the attacker, you can use your reaction to impose disadvantage on the roll (once per turn).

**Level 11 — Drunken Monologue**
- When you take the Dodge action on your turn, you can use a bonus action to make one unarmed strike.
- When you take Flurry of Blows, you can add an extra unarmed strike (3 strikes total instead of 2, but costs 1 extra ki).

**Level 17 — Intoxicated Frenzy**
- When you take the Attack action on your turn, you can replace one attack with a Flurry of Blows (no ki cost if you use Flurry as part of Attack).
- Your AC during Flurry increases to 11 + DEX + WIS (base change).

**Mechanical notes**: Drunken Master is an evasion/mobility subclass. Drunken Technique grants scaling AC and advantage on saves during Flurry, enabling high AC mobility. Tipsy Sway is an additional reaction defense. Drunken Monologue adds extra attacks to Dodge (action economy). Intoxicated Frenzy chains Flurry into Attack action, multiplying strike count.

---

### Way of the Kensei

**Level 3 — Kensei Weapons**
- You gain proficiency with any martial melee weapon (single-handed and two-handed, not ranged weapons) as a Kensei weapon.
- When you hit with a Kensei weapon, you can use a bonus action to make an unarmed strike.
- When you hit with an unarmed strike, you can use a bonus action to attack with a Kensei weapon.
- You can apply your martial arts damage scaling to Kensei weapons (treat them as monk weapons for damage, DEX/STR mod, scaling dice).

**Level 3 — Agile Parry**
- When you are hit by a melee weapon attack while you're wielding a Kensei weapon, you can use your reaction to add your WIS modifier to your AC against that attack (before you know if it hits).
- Requires reaction and counts as a reaction per turn (not per attack).

**Level 6 — Kensei's Shot**
- When you take the Attack action, you can replace one of your attacks with a ranged attack using a Kensei weapon you can reach.
- Ranged attacks apply your DEX or STR modifier (martial arts scaling).
- You can add 1d4 to the damage roll (scales to 1d6 at 11, 1d8 at 17).

**Level 11 — One with the Blade**
- Once per turn, when you hit with a Kensei weapon, you can apply your WIS modifier to the damage roll (in addition to STR/DEX).
- This applies to unarmed strikes as bonus actions as well.

**Level 17 — Quickened Healing**
- When you use Flurry of Blows, you can spend 1 additional ki to regain 1d4 + WIS modifier HP (heals you, not an ally).

**Mechanical notes**: Kensei is a weapon-focused monk. Kensei Weapons lets you use any martial melee weapon with unarmed strike synergy. Agile Parry adds WIS to AC reactively (one reaction per turn). Kensei's Shot adds ranged attacks with scaling bonus dice. One with the Blade adds WIS to damage. Quickened Healing converts ki to healing.

---

### Way of the Sun Soul

**Level 3 — Radiant Sun Bolt**
- You can create a bolt of radiant energy as a ranged spell attack (uses your monk's unarmed strike damage, DEX/WIS for attack and damage).
- You can use a bonus action to throw a Sun Bolt after your Attack action (same as unarmed strike bonus actions with Martial Arts).
- Damage scales with Martial Arts die progression (d4/d6/d8/d10).

**Level 3 — Searing Arc Strike**
- When you cast a spell (not Radiant Sun Bolt) that forces creatures to make a save, creatures within 5 ft of you that fail have disadvantage on the save (gain advantage on your save DC).
- Once per turn.

**Level 6 — Searing Sunburst**
- When you hit a creature within 30 ft with Radiant Sun Bolt, you can spend 1 ki to deal an additional 1d6 radiant damage and each creature within 5 ft of the target takes 1d6 radiant damage (DEX save for half).
- Uses ki but doesn't consume the normal attack.

**Level 11 — Sun Shield**
- Reaction when you take fire or radiant damage, you can reduce it by 1d10 + WIS modifier.
- Once per long rest (recharges).

**Level 17 — Blazing Crescendo**
- When you take the Attack action, you can use a bonus action to make a Radiant Sun Bolt attack. If it hits, each creature within 5 ft of the target takes 1d6 radiant damage.
- Once per turn, triggered by your action economy.

**Mechanical notes**: Sun Soul is a radiant spell-casting monk. Radiant Sun Bolt is a ranged attack with unarmed scaling. Searing Arc Strike adds debuff to spell saves. Searing Sunburst is a conical AoE damage add-on (ki cost). Sun Shield is damage reduction (once per long rest). Blazing Crescendo multiplies attacks by adding radiant AoE to Attack actions.

---

## Paladin

**Subclass gained at Level 3 (Sacred Oath)**

### Oath of Conquest

**Level 3 — Bonus Proficiencies**
- Martial weapons (PHB list).

**Level 3 — Oath Spells**
- Always prepared: *Armor of Agathys* (reflects damage when hit), *Command* (control save).
- At 5: *Hold Person* (paralyze save), *Spiritual Weapon* (flying melee attacker).
- At 9: *Bestow Curse* (save, -4 to rolls), *Dispel Magic* (remove spells).
- At 13: *Dominate Beast* (charmed condition), *Stoneskin* (damage reduction).
- At 17: *Cloudkill* (save, 5d8 poison AoE), *Dominate Person* (charmed condition).

**Level 3 — Channel Divinity: Conquering Strike**
- When you hit with a melee weapon attack, you can use your Channel Divinity to add damage = 1d8 + CHA modifier radiant damage.
- If the target is a creature, it must make a WIS save (spell DC). On fail, it's knocked prone.
- Once per short rest.

**Level 7 — Aura of Conquest**
- Creatures within 30 ft (10 ft at 6, 30 ft at 18) that are frightened of you have their speed reduced to 0 (can't move).
- If a creature is frightened and within your aura, when it enters your aura or starts its turn there, it takes 2d6 psychic damage (no save).

**Level 15 — Scourge of the Faithless**
- Creatures within 30 ft that you hit with a melee weapon attack and reduce to 0 HP don't gain death saving throw benefits — they die outright if they have no allies within 30 ft.
- This is a save-based insta-kill trigger: "if reduced to 0 HP, you die unless you have an ally nearby."

**Level 20 — Invincible Conqueror**
- Action to assume a conqueror form for 1 minute. During that time:
  - You have resistance to all damage.
  - When you hit with a melee weapon attack, you gain +4 weapon damage.
  - Creatures within 30 ft that you can see have disadvantage on saves against your spells and Channel Divinity.
- Once per long rest.

**Mechanical notes**: Conquest is an aggressive, control-focused oath. Conquering Strike adds damage and knocks prone. Aura of Conquest immobilizes frightened creatures and deals damage to them each turn. Scourge of the Faithless is a conditional insta-kill (no allies nearby). Invincible Conqueror is a powerful buff action (resistance, damage boost, spell debuff).

---

### Oath of Redemption

**Level 3 — Bonus Proficiencies**
- Insight, Persuasion (if not already).

**Level 3 — Oath Spells**
- Always prepared: *Sanctuary* (no attacks in area), *Sleep* (save, unconscious).
- At 5: *Calm Emotions* (save, suppress emotions), *Hold Person* (paralyze).
- At 9: *Counterspell* (reaction, prevent spell), *Hypnotic Pattern* (save, incapacitate).
- At 13: *Otiluke's Resilient Sphere* (save, containment bubble), *Wall of Force* (spell barrier).
- At 17: *Circle of Power* (20 ft aura, save bonus), *Wall of Thorns* (damage barrier).

**Level 3 — Channel Divinity: Emissary of Peace**
- Action to grant yourself and allies within 30 ft advantage on attack rolls and saves until the end of your next turn.
- Once per short rest.

**Level 7 — Protective Spirit**
- Reaction when a creature within 30 ft that you can see takes damage, you can expend a spell slot to reduce the damage by 5 × the spell slot level (1st slot = 5 damage reduction, 5th = 25 damage).
- No limit on uses per turn (only spell slots matter).

**Level 15 — Redemption**
- Reaction when a creature within 30 ft is hit by an attack roll or spell save, you can use your reaction to impose disadvantage on that roll/save and then deal 2d10 radiant damage to the attacker.
- Once per long rest.

**Level 20 — Emissary of Redemption**
- Whenever a creature deals damage to you, that creature takes an equal amount of radiant damage (no action or reaction required).
- This triggers whenever you take damage, damage reflection is automatic.

**Mechanical notes**: Redemption is a defensive, healing-focused oath. Emissary of Peace grants advantage broadly. Protective Spirit is efficient damage reduction (5 per spell level). Redemption is a penalty to hostile rolls plus damage back. Emissary of Redemption is automatic damage reflection whenever you take any damage (powerful for tanking).

---

## Ranger

**Subclass gained at Level 3 (Ranger Archetype)**

### Gloom Stalker

**Level 3 — Dread Ambusher**
- When you roll initiative and don't have any Dread Stalker uses active, you regain 1 use.
- When you take the Attack action on your first turn of combat, you can make one additional weapon attack (add one extra attack roll and damage roll).
- You gain +10 ft movement speed during your first turn of combat. This movement doesn't provoke opportunity attacks.
- Dread Ambusher resets at the start of combat (initiative roll triggers the reset, not per-session).

**Level 3 — Umbral Sight**
- You gain advantage on Perception checks (Wisdom (Perception)) in dim light or darkness.
- When you attack a target in dim light or darkness, the target has disadvantage on the attack roll against you (works even if the target can see you).

**Level 5 — Extra Attack**
- Make two attacks with your Attack action (standard ranger feature, included in the subclass).

**Level 7 — Iron Mind**
- You have advantage on saves vs. being charmed or frightened.
- You're immune to magical effects that sense your emotions or read your thoughts.

**Level 11 — Stalker's Flurry**
- Once per turn when you miss with a weapon attack, you can make another weapon attack as part of the same action (bonus action attack).
- The extra attack uses the same bonus action economy as regular bonus actions.

**Level 15 — Shadowy Dodge**
- Reaction when a creature within 5 ft makes an attack roll against you and you're in dim light or darkness, you can impose disadvantage on the roll.
- Once per turn.

**Mechanical notes**: Gloom Stalker is an ambush/darkness specialist. Dread Ambusher grants extra attack on first turn (initiative resets uses). Umbral Sight adds advantage in darkness. Iron Mind prevents emotional control. Stalker's Flurry adds bonus attacks on misses. Shadowy Dodge imposes disadvantage in darkness (reaction).

---

### Horizon Walker

**Level 3 — Detect Portal**
- You can cast *detect magic* at will, sensing only planar portals within 1 mile (concentration not required if cast at will).
- As a bonus action, you can sense planar portals within 1 mile (action cost to use detect magic normally).

**Level 3 — Planar Warrior**
- Once per turn when you hit with a weapon attack, you can expend 1 use of this feature to add 1d8 force damage (scales to 1d10 at 11).
- Uses = WIS modifier (minimum 1) per short rest.

**Level 5 — Extra Attack**
- Make two attacks with your Attack action.

**Level 7 — Ethereal Step**
- Bonus action to become invisible and insubstantial (ethereal) for 1 minute or until you attack/cast a spell. When ethereal, you can't be hit (resistance to all damage except force and psychic).
- Uses = WIS modifier per short rest.

**Level 11 — Distant Strike**
- When you use Planar Warrior, you can teleport up to 30 ft to an unoccupied space you can see before making the attack (teleportation costs no action, happens as part of the attack).

**Level 15 — Spectral Defense**
- Reaction when you take damage from a source you can see, you can reduce the damage by 1d8 + WIS modifier.
- Once per long rest.

**Mechanical notes**: Horizon Walker is a teleporting, force-damage specialist. Detect Portal enables planar sense. Planar Warrior adds d8-d10 force damage on hits (WIS mod uses per rest). Ethereal Step is evasion/invisibility (WIS mod uses per rest). Distant Strike teleports before attacks. Spectral Defense reduces damage once per long rest.

---

### Monster Slayer

**Level 3 — Hunter's Sense**
- As a bonus action, you can sense the presence of creatures within 1 mile. You know their location, type (beast, undead, etc.), and a general sense of their hit points (bloodied, healthy).
- You can dismiss the sense as a bonus action.

**Level 3 — Slayer's Prey**
- Bonus action to choose a creature within 60 ft as your prey. Until you finish a short or long rest, you gain:
  - Advantage on Wisdom (Perception) checks and Survival checks to track the prey.
  - Whenever you hit the prey with a weapon attack, add 1d6 damage (scales to 1d8 at 11).
  - You can sense the prey's location within 1 mile (as an action, you can determine the exact range and direction).
- Only one prey at a time.

**Level 5 — Extra Attack**
- Make two attacks with your Attack action.

**Level 7 — Supernatural Defense**
- Reaction when you take damage from a creature within 30 ft that you can see, you can impose disadvantage on the attack roll (if it's an attack) or reduce the damage by 1d6 + WIS modifier (if it's not).

**Level 11 — Magic-User's Nemesis**
- Reaction when a creature within 30 ft casts a spell and you can see them, you can use your reaction to impose disadvantage on the save DC of the spell (creatures have disadvantage on saves, not guaranteed fail).
- Once per turn.

**Level 15 — Slayer's Counter**
- Reaction when a creature misses you with an attack, you can make a weapon attack against that creature (if you can reach them with your weapon).
- Once per turn.

**Mechanical notes**: Monster Slayer is a focused tracker/damage specialist. Hunter's Sense reveals creatures in range. Slayer's Prey marks a target for bonus damage and tracking. Supernatural Defense applies disadvantage or damage reduction. Magic-User's Nemesis penalizes spell saves. Slayer's Counter grants bonus attacks from misses.

---

## Rogue

**Subclass gained at Level 3 (Roguish Archetype)**

### Inquisitive

**Level 3 — Ear for Deception**
- Advantage on Insight checks to determine if a creature is lying.
- You also gain advantage on Perception checks to notice hidden creatures or objects within 10 ft.

**Level 3 — Insightful Fighting**
- Bonus action to make a Wisdom (Insight) check against a creature's Charisma (Deception) check. If you win, you gain advantage on attack rolls against that creature until the end of your next turn (uses your INT or WIS mod, you choose).
- No limit on uses (bonus action per turn).

**Level 9 — Steady Eye**
- You don't have disadvantage on Perception checks when you're within 5 ft of a creature (normally rogues get disadvantage in melee).
- When a creature within 30 ft uses stealth, you can use your reaction to see them (they fail their Stealth check against you).

**Level 9 — Unerring Eye**
- When you make a Perception or Insight check against a creature you can see, you can add your proficiency bonus to the check (if you're already proficient, you gain advantage instead).

**Level 13 — Eye for Weakness**
- Your Sneak Attack damage increases by 1d6 (adds to your normal Sneak Attack progression, not replaces).
- When you have advantage on an attack roll against a creature, your Sneak Attack uses the higher damage roll.

**Level 17 — Slippery Mind**
- Reaction when you make a saving throw, you can roll a d4 and add the result to the save (if you fail, you can still use this reaction).
- Once per long rest.

**Mechanical notes**: Inquisitive is an insight/deception specialist. Insightful Fighting grants advantage on attacks with an Insight check (bonus action check, scales). Ear for Deception adds advantage to Insight. Unerring Eye prevents perception disadvantage in melee and triggers Stealth success negation. Eye for Weakness adds Sneak Attack damage. Slippery Mind adds saves once per long rest.

---

### Mastermind

**Level 3 — Master of Intrigue**
- You gain proficiency in one of: Deception, Insight, Investigation, Persuasion.
- You can mimic accents/speech patterns and forge documents (handwriting, seals) with an hour of work and Deception check (DC = target's Insight check).

**Level 3 — Master of Tactics**
- Bonus action, you choose an ally within 30 ft and a creature within 5 ft of you that your ally can see. Your ally gains advantage on the next attack roll against that creature before the end of your next turn (no roll needed, just granting advantage).
- Uses = 1 per short rest (scales to more uses at higher levels, but no level-based progression in XGtE errata).

**Level 9 — Insightful Manipulator**
- When you make a Charisma (Deception) or Charisma (Persuasion) check, you can add your proficiency bonus to the roll (if you're already proficient, gain advantage).
- You gain insight into creatures' feelings when you speak with them (no save, you just know if they're friendly, indifferent, hostile, or scared).

**Level 9 — Use Magic Device**
- You can use magic items and activate them (cast spells from items) with no proficiency requirement. You can touch magic items to learn what they do without using them.

**Level 13 — Ambush Master**
- When you take the Hide action, you can use a bonus action to make a melee attack against a creature within 5 ft (attacking ends your hidden state, same as normal).
- When you're hidden and hit with an attack, you don't reveal your position until after you've dealt damage.

**Level 17 — Soul of Intrigue**
- You can cast *detect thoughts* once per long rest, using CHA instead of INT (no spell slots required).
- When you cast it, you gain an additional use when you finish a short or long rest (up to 2 uses total, but resets per long rest).

**Mechanical notes**: Mastermind is a social engineering rogue. Master of Tactics grants advantage to allies (bonus action). Insightful Manipulator adds proficiency to social checks. Use Magic Device removes item proficiency restrictions. Ambush Master adds attacks from Hide action. Soul of Intrigue enables *detect thoughts* once per rest.

---

### Scout

**Level 3 — Skirmisher**
- Reaction when a creature within 5 ft moves away from you, you can move up to half your speed without provoking opportunity attacks (no action cost).
- Once per turn.

**Level 3 — Tactical Advantage**
- Whenever you don't move more than half your speed on your turn, you gain advantage on attack rolls against creatures within 5 ft.
- If you move more than half your speed, you don't gain the advantage.

**Level 9 — Superior Mobility**
- You gain +10 ft movement speed.
- You don't trigger opportunity attacks when you move away from creatures (ending your turn doesn't prevent attacks, only moving away does).

**Level 9 — Ambush Tactics**
- When you're hidden and you make a ranged attack, you don't lose your hidden state (even if you hit, you stay hidden).
- You can use a bonus action to move stealthily (Dash and Disengage as part of your bonus action).

**Level 13 — Sudden Strike**
- You can use your Sneak Attack even if you don't have advantage, as long as an ally within 5 ft of the target doesn't have disadvantage on attack rolls.
- Sneak Attack still requires a ranged weapon attack or a melee weapon attack with finesse/light weapon.

**Level 17 — Evasion**
- Reaction when you make a DEX save for half damage, if you succeed, you take no damage instead (and if you fail, you take half as normal).
- Once per turn.

**Mechanical notes**: Scout is a mobility/repositioning rogue. Skirmisher is a reaction retreat. Tactical Advantage grants advantage when you don't move much. Superior Mobility adds speed and removes opportunity attacks. Ambush Tactics enables hidden ranged attacks. Sudden Strike removes Sneak Attack advantage requirement (uses ally positioning instead). Evasion is a save-based negation of damage once per turn.

---

### Swashbuckler

**Level 3 — Fancy Footwork**
- When you use the Dash action on your turn, you can move within 5 ft of a hostile creature without provoking opportunity attacks that turn.
- You can move away from hostiles during Dash or normal movement (movement type doesn't matter, just being within 5 ft).

**Level 3 — Rakish Audacity**
- You can use CHA instead of DEX for initiative.
- When you make a melee weapon attack as part of your Attack action, you can roll a d6 and add the result to the damage (scales to d8 at 9, d10 at 13).
- This is a scaling bonus damage die, added to each attack once per turn (not per attack).

**Level 9 — Panache**
- Reaction when a creature within 5 ft makes an attack roll against you, you can use your reaction to move up to half your speed without provoking opportunity attacks (takes place before the attack is resolved).
- Once per turn.

**Level 9 — Parry**
- Reaction when a creature within 5 ft makes a melee attack against you, you can use your reaction to add 1d6 to your AC (subtracted from the attack roll).
- Once per turn.

**Level 13 — Elegant Maneuver**
- Bonus action to take the Disengage or Dodge action (not extra action, bonus action Disengage/Dodge).

**Level 17 — Master Duelist**
- Reaction when you hit with a melee weapon attack, you can roll a d6 and add it to the damage roll (in addition to Rakish Audacity's bonus).
- Once per long rest.

**Mechanical notes**: Swashbuckler is an evasion/duelist rogue. Fancy Footwork prevents opportunity attacks during movement (synergizes with Dash). Rakish Audacity adds a scaling d6-d10 bonus damage die. Panache is a reaction dodge. Parry adds AC reactively (d6 bonus). Elegant Maneuver enables bonus action Disengage/Dodge. Master Duelist adds damage on hits once per rest.

---

## Sorcerer

**Subclass gained at Level 1 (Sorcerous Origin)**

### Divine Soul

**Level 1 — Divine Magic**
- You learn 2 spells from the Cleric spell list (in addition to your Sorcerer spells known).
- You can cast these spells using Sorcerer spell slots.
- At 5, 9, 13, 17, you learn 2 more Cleric spells.

**Level 1 — Favored by the Gods**
- Reaction when you make a saving throw or attack roll, you can expend 2 Sorcery Points to add 2d4 to the roll (after rolling but before the outcome is determined).
- No limit on uses per turn (only Sorcery Points matter).

**Level 6 — Empowered Healing**
- When you cast a spell that restores HP, you can spend 1 Sorcery Point per die rolled to reroll the healing (choose the new result or original).
- You can reroll multiple times if you have points.

**Level 14 — Blessed Strikes**
- When you hit a creature with a weapon attack or when a creature fails on a save against your spell, you can deal 1d8 extra radiant damage to that creature.
- Once per turn.

**Level 18 — Divine Intervention**
- Once per long rest, you can take an action to plead for aid (equivalent to divine intervention).
- Roll a d100. If the result ≤ your Sorcerer level + CHA mod, you can cast a spell of 5th level or lower without using a spell slot (DM determines the effect if you don't request a specific spell).

**Mechanical notes**: Divine Soul is a full caster with healing focus. Divine Magic adds Cleric spells to your list. Favored by the Gods is a reaction boost (2d4 per 2 Sorcery Points). Empowered Healing converts Sorcery Points to reroll healing dice. Blessed Strikes adds radiant damage to hits/spell saves. Divine Intervention is a once-per-rest utility option.

---

### Shadow Magic

**Level 1 — Eyes of Darkness**
- You gain darkvision 120 ft.
- You can cast *darkness* at will (no spell slots, no components needed, but you must spend 2 Sorcery Points). Creatures in the darkness you create have disadvantage on saves and attacks against you.

**Level 1 — Strength of the Grave**
- When you take damage and you have at least 1 HP, you can use your reaction to reduce the damage by 1d4 + CHA modifier.
- Once per long rest.

**Level 6 — Hound of Ill Omen**
- Bonus action, you summon a hound made of shadow in an unoccupied space within 30 ft (lasts 1 minute, concentration-free). The hound uses your action to move and bite:
  - Bite: melee attack against a creature within 5 ft, +CHA mod to hit, deals 2d6 psychic damage on hit.
  - When a creature attacks you while the hound is within 30 ft, the hound can use its reaction to bite the attacker (with disadvantage if the attacker can't see the hound).
- Uses = CHA modifier (minimum 1) per long rest.

**Level 14 — Shadow Walk**
- When you're in an area of dim light or darkness, you can use your bonus action to magically turn invisible (lasts until you move or take an action/reaction).
- Once per short rest.

**Level 18 — Umbral Form**
- Action to transform into a shadow for 1 minute (or until you end it as a bonus action). While transformed:
  - You're invisible in dim light or darkness.
  - You can move through other creatures and objects as if they were difficult terrain (5 ft per 5 ft moved, can't end your turn inside an object).
  - You take 5 extra damage from radiant sources.
- Uses = 1 per long rest.

**Mechanical notes**: Shadow Magic is a stealth/control sorcerer. Eyes of Darkness grants 120 ft darkvision and at-will darkness (2 Sorcery Points per cast). Strength of the Grave is damage reduction once per rest (reaction). Hound of Ill Omen summons an attacker (CHA mod uses per rest). Shadow Walk grants invisibility in darkness (bonus action). Umbral Form is a transformation enabling movement through objects.

---

### Storm Sorcery

**Level 1 — Wind Speaker**
- You learn the *prestidigitation* cantrip (doesn't count toward cantrips known).
- You can create minor atmospheric effects with *prestidigitation* (wind, lightning flashes, thunder sounds).

**Level 1 — Tempestuous Magic**
- When you cast a spell, you can use a bonus action to move your flying speed in a straight line (if you have flying speed). This movement doesn't provoke opportunity attacks.
- If you don't have flying speed, you gain +10 ft movement speed until the end of your turn after casting a spell.

**Level 6 — Heart of the Storm**
- You gain resistance to lightning and thunder damage.
- When you finish a long rest, you gain temporary HP = your Sorcerer level (resets each rest).

**Level 6 — Storm Guide**
- You can modify the wind and weather within 300 ft when you finish a long rest (you control rain, fog, etc., but you can't summon creatures, cause lightning, etc.).
- Effects last until your next rest or you dismiss them (action).

**Level 14 — Storm's Fury**
- Reaction when a creature within 30 ft casts a spell and you can see them, you can use your reaction to deal 1d6 lightning damage to that creature (no save).
- Once per turn.

**Level 18 — Wind Soul**
- Action to become surrounded by wind for 1 minute (or until you end it as a bonus action). While active:
  - You gain flying speed = your walking speed.
  - Ranged attacks against you have disadvantage (wind deflects projectiles).
  - You can move through other creatures as if they were difficult terrain.
- Uses = 1 per long rest.

**Mechanical notes**: Storm Sorcery is a flight-and-control sorcerer. Tempestuous Magic adds movement after spellcasting (flight speed if you have it, movement if not). Heart of the Storm grants lightning/thunder resistance and temp HP. Storm Guide enables weather control. Storm's Fury deals damage to spellcasters (reaction). Wind Soul is a flight-granting transformation.

---

## Warlock

**Subclass gained at Level 1 (Otherworldly Patron)**

### The Celestial

**Level 1 — Bonus Cantrips**
- You learn *light* and one cleric cantrip of your choice (doesn't count toward cantrips known). You can cast *light* on yourself without components (instant cast, no action).

**Level 1 — Healing Light**
- You gain a pool of healing HP = Warlock level × 1d8 + CHA modifier (e.g., 3 Warlock = 3 to 24 HP in pool at +3 CHA).
- When you or a creature within 60 ft takes damage, you can use your reaction to restore that creature HP from the pool (no limit on uses per turn, only pool size matters).
- The pool recharges at the start of each long rest.

**Level 6 — Radiant Soul**
- When you cast a spell that deals damage, you can add CHA modifier to one roll of that spell (for example, *eldritch blast* hit gets +CHA damage per bolt).
- You add CHA modifier to the damage of spells you cast.

**Level 10 — Protective Light**
- You can use your reaction to reduce damage taken by a creature within 60 ft by 1d6 + WIS modifier (no limit on uses per turn).
- When a creature you can see within 60 ft makes a saving throw, they add 1d4 to the save.

**Level 14 — Celestial Resilience**
- You have resistance to radiant damage.
- When you finish a short or long rest, you and up to 5 allies of your choice within 10 ft gain temporary HP = 1d8 + WIS modifier.

**Mechanical notes**: Celestial is a healing-focused warlock. Healing Light is a resource pool (recharged per long rest) used reactively to restore HP. Radiant Soul adds CHA to damage rolls on spells. Protective Light is damage reduction (1d6 + WIS, no limit). Celestial Resilience grants temp HP on rest.

---

### The Hexblade

**Level 1 — Hexblade's Curse**
- Bonus action, choose a creature within 30 ft. For 1 minute, you gain these benefits against that target:
  - Weapon attacks use CHA instead of STR/DEX for attack and damage rolls (against this one target).
  - When you hit the target, you deal extra 1d6 psychic damage.
  - If the target drops to 0 HP before the minute ends, you can use your bonus action on your next turn to curse another creature.
- Uses = 1 per short rest (2 at level 5, 3 at level 11, etc.).

**Level 1 — Medium Armor and Shield Proficiency**
- Proficiency with medium armor and shields. (Warlocks don't normally get this.)

**Level 6 — Accursed Specter**
- When you hit with a weapon attack while Hexblade's Curse is active on the target, if the target has fewer hit points than half its hit point maximum, the target makes a WIS save (spell DC) or is frightened of you until the end of your next turn.

**Level 10 — Armor of Hexes**
- Reaction when an attacker within 30 ft makes an attack roll against you, you can impose disadvantage on that roll (once per turn).

**Level 14 — Master of Hexes**
- When you hit a creature with a weapon attack while Hexblade's Curse is active on them, the curse transfers to the next creature you curse with Hexblade's Curse (you don't need to recast, the curse "sticks" to targets).
- If you hit a creature and reduce them to 0 HP, you regain all uses of Hexblade's Curse (curse resets).

**Mechanical notes**: Hexblade is a melee-focused, CHA-scaling warlock. Hexblade's Curse adds 1d6 psychic damage and enables CHA scaling on attacks (one target at a time). Accursed Specter applies fear. Armor of Hexes is disadvantage on attack rolls. Master of Hexes transfers the curse and resets on kills.

---

## Wizard

**Subclass gained at Level 2 (Arcane Tradition)**

### War Magic

**Level 2 — Arcane Deflection**
- Reaction when you take damage while you can see the attacker (or when hit by a spell attack), you can spend 1 reaction to add your INT modifier to your AC against the attack (before you know if it hits, retroactive).
- Or, you can reduce the damage by 1d4 + INT modifier (after the damage is rolled).
- Once per turn.

**Level 2 — Tactical Wit**
- You add your INT modifier to your initiative rolls.

**Level 6 — Power Surge**
- Whenever you finish a short rest, you gain 1 Power Surge charge (up to your INT modifier, minimum 1). You can expend a charge when you hit with a spell attack or when a creature fails a save against your spell to add 1d8 damage (or add 1d8 to any damage roll of that spell).
- Charges don't carry over between rests.

**Level 10 — Durable Magic**
- When you cast an abjuration spell, you gain temporary HP = the spell's level (minimum 1).
- Or, when you cast any spell and use Arcane Deflection, you gain 1d4 temporary HP (uses the same reaction).

**Level 14 — Tactical Mastery**
- When you use your action to cast a spell, you can use your bonus action to take the Dodge or Disengage action.
- Once per turn.

**Mechanical notes**: War Magic is a reaction-heavy, control-focused wizard. Arcane Deflection is a reaction AC/damage reduction. Tactical Wit adds INT to initiative. Power Surge charges damage on spell hits/saves (INT mod charges per rest). Durable Magic grants temp HP on abjuration casts. Tactical Mastery enables bonus action Dodge/Disengage when casting spells.

---

## Index & Notes

This document covers all 24 XGtE subclasses (2-3 per base class) with mechanical details sufficient for LLM game mastering. Features are listed with levels, action economy, uses/recharge, damage dice, saving throw DCs, and resource pools. All numerical scaling is included (where applicable).

For spell DCs and attack modifiers not specified in subclass features, use the character's spell attack bonus (INT/WIS/CHA + proficiency) and spell save DC (8 + spellcasting ability modifier + proficiency).

