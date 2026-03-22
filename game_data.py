STANDARD_ARRAY = [15, 14, 13, 12, 10, 8]

ABILITY_SCORES = ["STR", "DEX", "CON", "INT", "WIS", "CHA"]

ABILITY_NAMES = {
    "STR": "Strength",
    "DEX": "Dexterity",
    "CON": "Constitution",
    "INT": "Intelligence",
    "WIS": "Wisdom",
    "CHA": "Charisma",
}

SKILLS = {
    "Acrobatics":     "DEX",
    "Animal Handling":"WIS",
    "Arcana":         "INT",
    "Athletics":      "STR",
    "Deception":      "CHA",
    "History":        "INT",
    "Insight":        "WIS",
    "Intimidation":   "CHA",
    "Investigation":  "INT",
    "Medicine":       "WIS",
    "Nature":         "INT",
    "Perception":     "WIS",
    "Performance":    "CHA",
    "Persuasion":     "CHA",
    "Religion":       "INT",
    "Sleight of Hand":"DEX",
    "Stealth":        "DEX",
    "Survival":       "WIS",
}

# Races: asi = fixed bonuses, flex_asi = number of additional +1s player assigns freely (Half-Elf)
RACES = {
    "Human": {
        "asi": {"STR": 1, "DEX": 1, "CON": 1, "INT": 1, "WIS": 1, "CHA": 1},
        "speed": 30, "size": "Medium",
        "traits": ["Extra Language"],
        "languages": ["Common", "One of your choice"],
    },
    "Elf (High)": {
        "asi": {"DEX": 2, "INT": 1},
        "speed": 30, "size": "Medium",
        "traits": ["Darkvision 60 ft", "Keen Senses (Perception proficiency)", "Fey Ancestry", "Trance", "Wizard Cantrip"],
        "languages": ["Common", "Elvish", "One of your choice"],
    },
    "Elf (Wood)": {
        "asi": {"DEX": 2, "WIS": 1},
        "speed": 35, "size": "Medium",
        "traits": ["Darkvision 60 ft", "Keen Senses (Perception proficiency)", "Fey Ancestry", "Trance", "Fleet of Foot", "Mask of the Wild"],
        "languages": ["Common", "Elvish"],
    },
    "Elf (Drow)": {
        "asi": {"DEX": 2, "CHA": 1},
        "speed": 30, "size": "Medium",
        "traits": ["Superior Darkvision 120 ft", "Sunlight Sensitivity", "Drow Magic", "Drow Weapon Training"],
        "languages": ["Common", "Elvish"],
    },
    "Dwarf (Hill)": {
        "asi": {"CON": 2, "WIS": 1},
        "speed": 25, "size": "Medium",
        "traits": ["Darkvision 60 ft", "Dwarven Resilience", "Dwarven Combat Training", "Stonecunning", "Dwarven Toughness (+1 HP/level)"],
        "languages": ["Common", "Dwarvish"],
    },
    "Dwarf (Mountain)": {
        "asi": {"STR": 2, "CON": 2},
        "speed": 25, "size": "Medium",
        "traits": ["Darkvision 60 ft", "Dwarven Resilience", "Dwarven Combat Training", "Dwarven Armor Training", "Stonecunning"],
        "languages": ["Common", "Dwarvish"],
    },
    "Halfling (Lightfoot)": {
        "asi": {"DEX": 2, "CHA": 1},
        "speed": 25, "size": "Small",
        "traits": ["Lucky", "Brave", "Halfling Nimbleness", "Naturally Stealthy"],
        "languages": ["Common", "Halfling"],
    },
    "Halfling (Stout)": {
        "asi": {"DEX": 2, "CON": 1},
        "speed": 25, "size": "Small",
        "traits": ["Lucky", "Brave", "Halfling Nimbleness", "Stout Resilience"],
        "languages": ["Common", "Halfling"],
    },
    "Gnome (Rock)": {
        "asi": {"INT": 2, "CON": 1},
        "speed": 25, "size": "Small",
        "traits": ["Darkvision 60 ft", "Gnome Cunning", "Artificer's Lore", "Tinker"],
        "languages": ["Common", "Gnomish"],
    },
    "Gnome (Forest)": {
        "asi": {"INT": 2, "DEX": 1},
        "speed": 25, "size": "Small",
        "traits": ["Darkvision 60 ft", "Gnome Cunning", "Natural Illusionist", "Speak with Small Beasts"],
        "languages": ["Common", "Gnomish"],
    },
    "Half-Elf": {
        "asi": {"CHA": 2},
        "flex_asi": 2,  # player picks +1 to two different ability scores
        "speed": 30, "size": "Medium",
        "traits": ["Darkvision 60 ft", "Fey Ancestry", "Skill Versatility (2 free skills)", "+1 to two ability scores of your choice"],
        "languages": ["Common", "Elvish", "One of your choice"],
    },
    "Half-Orc": {
        "asi": {"STR": 2, "CON": 1},
        "speed": 30, "size": "Medium",
        "traits": ["Darkvision 60 ft", "Menacing (Intimidation proficiency)", "Relentless Endurance", "Savage Attacks"],
        "languages": ["Common", "Orc"],
    },
    "Dragonborn": {
        "asi": {"STR": 2, "CHA": 1},
        "speed": 30, "size": "Medium",
        "traits": ["Draconic Ancestry", "Breath Weapon", "Damage Resistance (chosen damage type)"],
        "languages": ["Common", "Draconic"],
    },
    "Tiefling": {
        "asi": {"CHA": 2, "INT": 1},
        "speed": 30, "size": "Medium",
        "traits": ["Darkvision 60 ft", "Hellish Resistance (fire)", "Infernal Legacy (Thaumaturgy, Hellish Rebuke, Darkness)"],
        "languages": ["Common", "Infernal"],
    },
}

# MotM / TCoE races: flex_asi = "motm" means +2 to one score and +1 to a different score (player's choice).
# Custom Lineage: flex_asi = "custom" means +2 to one score of your choice.
# All MotM races have asi: {} (no fixed bonus).
MULTIVERSE_RACES = {
    "Aarakocra": {
        "asi": {}, "flex_asi": "motm",
        "speed": "30 ft / 30 ft flying", "size": "Medium",
        "traits": ["Flight 30 ft (no medium/heavy armor)", "Talons (1d6+STR slashing)", "Wind Caller (Gust of Wind 1/long rest)"],
        "languages": ["Common", "One of your choice"],
    },
    "Aasimar": {
        "asi": {}, "flex_asi": "motm",
        "speed": "30 ft", "size": "Medium or Small",
        "traits": ["Darkvision 60 ft", "Celestial Resistance (necrotic & radiant)", "Healing Hands (PB HP, PB/long rest)", "Light Bearer (Light cantrip)", "Celestial Revelation at Level 3 (Necrotic Shroud / Radiant Consumption / Radiant Soul)"],
        "languages": ["Common", "One of your choice"],
    },
    "Bugbear": {
        "asi": {}, "flex_asi": "motm",
        "speed": "30 ft", "size": "Medium",
        "traits": ["Darkvision 60 ft", "Fey Ancestry", "Long-Limbed (+5 ft melee reach on your turn)", "Powerful Build", "Sneaky (Stealth proficiency)", "Surprise Attack (2d6 extra vs. creatures that haven't acted, 1/combat)"],
        "languages": ["Common", "One of your choice"],
    },
    "Centaur": {
        "asi": {}, "flex_asi": "motm",
        "speed": "40 ft", "size": "Medium",
        "traits": ["Charge (bonus action hooves attack after 30 ft straight move)", "Equine Build (Powerful Build; climbing costs 4× movement)", "Hooves (1d6+STR bludgeoning)", "Natural Affinity (one skill: Animal Handling, Medicine, Nature, or Survival)"],
        "languages": ["Common", "One of your choice"],
    },
    "Changeling": {
        "asi": {}, "flex_asi": "motm",
        "speed": "30 ft", "size": "Medium or Small",
        "traits": ["Shapechanger (appear as any humanoid, action)", "Changeling Instincts (2 skills from: Deception, Insight, Intimidation, Persuasion)"],
        "languages": ["Common", "Two of your choice"],
    },
    "Deep Gnome": {
        "asi": {}, "flex_asi": "motm",
        "speed": "30 ft", "size": "Small",
        "traits": ["Darkvision 120 ft", "Gnome Cunning (advantage on INT/WIS/CHA saves vs. magic)", "Gift of the Svirfneblin (Disguise Self 1/lr; Nondetection at 3rd; Blindness/Deafness at 5th)", "Svirfneblin Camouflage (advantage on Stealth in rocky terrain)"],
        "languages": ["Common", "Gnomish", "Undercommon"],
    },
    "Duergar": {
        "asi": {}, "flex_asi": "motm",
        "speed": "30 ft", "size": "Medium",
        "traits": ["Darkvision 120 ft", "Duergar Resilience (advantage vs. poison/charmed/stunned; resist poison)", "Psionic Fortitude (advantage vs. charmed/stunned)", "Duergar Magic (Enlarge at 3rd; Invisibility at 5th; 1/lr)", "Sunlight Sensitivity"],
        "languages": ["Common", "Dwarvish"],
    },
    "Eladrin": {
        "asi": {}, "flex_asi": "motm",
        "speed": "30 ft", "size": "Medium",
        "traits": ["Darkvision 60 ft", "Fey Ancestry", "Trance (4-hour rest)", "Keen Senses (Perception proficiency)", "Fey Step (teleport 30 ft, PB/lr; seasonal rider: Autumn/Winter/Spring/Summer)"],
        "languages": ["Common", "Elvish"],
    },
    "Fairy": {
        "asi": {}, "flex_asi": "motm",
        "speed": "30 ft / 30 ft flying", "size": "Small",
        "traits": ["Flight 30 ft (no medium/heavy armor)", "Fairy Magic (Druidcraft cantrip; Faerie Fire at 3rd; Enlarge/Reduce at 5th; 1/lr)"],
        "languages": ["Common", "One of your choice"],
    },
    "Firbolg": {
        "asi": {}, "flex_asi": "motm",
        "speed": "30 ft", "size": "Medium",
        "traits": ["Firbolg Magic (Detect Magic & Disguise Self 1/lr; appear up to 3 ft shorter)", "Hidden Step (invisible until next turn start, PB/lr)", "Powerful Build", "Speech of Beast and Leaf"],
        "languages": ["Common", "One of your choice"],
    },
    "Genasi (Air)": {
        "asi": {}, "flex_asi": "motm",
        "speed": "35 ft", "size": "Medium or Small",
        "traits": ["Unending Breath (hold breath indefinitely)", "Lightning Resistance", "Mingle with the Wind (Shocking Grasp cantrip; Feather Fall at 3rd; Levitate at 5th; 1/lr)"],
        "languages": ["Common", "Primordial"],
    },
    "Genasi (Earth)": {
        "asi": {}, "flex_asi": "motm",
        "speed": "30 ft", "size": "Medium or Small",
        "traits": ["Earth Walk (ignore difficult terrain of earth/stone)", "Merge with Stone (Blade Ward cantrip; Pass Without Trace at 5th; 1/lr)"],
        "languages": ["Common", "Primordial"],
    },
    "Genasi (Fire)": {
        "asi": {}, "flex_asi": "motm",
        "speed": "30 ft", "size": "Medium or Small",
        "traits": ["Darkvision 60 ft", "Fire Resistance", "Reach to the Blaze (Produce Flame cantrip; Burning Hands at 3rd; Flame Blade at 5th; 1/lr)"],
        "languages": ["Common", "Primordial"],
    },
    "Genasi (Water)": {
        "asi": {}, "flex_asi": "motm",
        "speed": "30 ft / 30 ft swimming", "size": "Medium or Small",
        "traits": ["Amphibious (breathe air and water)", "Acid Resistance", "Call to the Wave (Acid Splash cantrip; Create/Destroy Water at 3rd; Water Walk at 5th; 1/lr)"],
        "languages": ["Common", "Primordial"],
    },
    "Githyanki": {
        "asi": {}, "flex_asi": "motm",
        "speed": "30 ft", "size": "Medium",
        "traits": ["Astral Knowledge (one skill + one weapon/tool proficiency per long rest)", "Githyanki Psionics (Mage Hand cantrip; Jump at 3rd; Misty Step at 5th; 1/lr)", "Psychic Resilience (resist psychic damage)"],
        "languages": ["Common", "One of your choice"],
    },
    "Githzerai": {
        "asi": {}, "flex_asi": "motm",
        "speed": "30 ft", "size": "Medium",
        "traits": ["Githzerai Psionics (Mage Hand cantrip; Shield at 3rd; Detect Thoughts at 5th; 1/lr)", "Mental Discipline (advantage vs. charmed and frightened)", "Psychic Resilience (resist psychic damage)"],
        "languages": ["Common", "One of your choice"],
    },
    "Goblin": {
        "asi": {}, "flex_asi": "motm",
        "speed": "30 ft", "size": "Small",
        "traits": ["Darkvision 60 ft", "Fey Ancestry", "Fury of the Small (extra PB damage vs. larger creatures, PB/lr)", "Nimble Escape (Disengage or Hide as bonus action, unlimited)"],
        "languages": ["Common", "One of your choice"],
    },
    "Goliath": {
        "asi": {}, "flex_asi": "motm",
        "speed": "30 ft", "size": "Medium",
        "traits": ["Little Giant (Powerful Build + Athletics proficiency)", "Mountain Born (cold resistance; no altitude sickness)", "Stone's Endurance (reduce damage by 1d12+CON as reaction, PB/lr)"],
        "languages": ["Common", "One of your choice"],
    },
    "Harengon": {
        "asi": {}, "flex_asi": "motm",
        "speed": "30 ft", "size": "Medium or Small",
        "traits": ["Hare-Trigger (+PB to initiative rolls)", "Leporine Senses (Perception proficiency)", "Lucky Footwork (add 1d4 to failed DEX save, PB/lr)", "Rabbit Hop (jump 5×PB ft as bonus action without OA, PB/lr)"],
        "languages": ["Common", "One of your choice"],
    },
    "Hobgoblin": {
        "asi": {}, "flex_asi": "motm",
        "speed": "30 ft", "size": "Medium",
        "traits": ["Darkvision 60 ft", "Fey Ancestry", "Fey Gift (Help as bonus action, PB/lr; riders at 3rd: temp HP / speed / save advantage)", "Fortune from the Many (add 1d6 to failed attack/check/save if ally nearby, PB/lr)"],
        "languages": ["Common", "One of your choice"],
    },
    "Kenku": {
        "asi": {}, "flex_asi": "motm",
        "speed": "30 ft", "size": "Medium or Small",
        "traits": ["Expert Duplication (advantage on forgery/duplicate checks)", "Kenku Recall (advantage on one proficient skill check, PB/lr)", "Mimicry (mimic sounds and voices heard)"],
        "languages": ["Common", "One of your choice"],
    },
    "Kobold": {
        "asi": {}, "flex_asi": "motm",
        "speed": "30 ft", "size": "Small",
        "traits": ["Darkvision 60 ft", "Draconic Cry (party advantage vs. enemies within 10 ft, bonus action, PB/lr)", "Kobold Legacy (choose one: Craftiness / Defiance / Draconic Sorcery)"],
        "languages": ["Common", "Draconic"],
    },
    "Lizardfolk": {
        "asi": {}, "flex_asi": "motm",
        "speed": "30 ft / 30 ft swimming", "size": "Medium",
        "traits": ["Bite (1d6+STR slashing)", "Hold Breath (15 minutes)", "Hungry Jaws (bonus action bite + temp HP equal to PB, PB/lr)", "Natural Armor (AC 13+DEX; stack with shield)", "Nature's Intuition (2 skills: Animal Handling, Medicine, Nature, Perception, Stealth, or Survival)"],
        "languages": ["Common", "One of your choice"],
    },
    "Minotaur": {
        "asi": {}, "flex_asi": "motm",
        "speed": "30 ft", "size": "Medium",
        "traits": ["Horns (1d6+STR piercing)", "Goring Rush (bonus action horn attack after Dash)", "Hammering Horns (bonus action shove after melee hit)", "Labyrinthine Recall (always know north; advantage vs. getting lost)"],
        "languages": ["Common", "One of your choice"],
    },
    "Orc": {
        "asi": {}, "flex_asi": "motm",
        "speed": "30 ft", "size": "Medium",
        "traits": ["Darkvision 60 ft", "Adrenaline Rush (Dash as bonus action + temp HP equal to PB, PB/lr)", "Powerful Build", "Relentless Endurance (drop to 1 HP instead of 0, 1/long rest)"],
        "languages": ["Common", "One of your choice"],
    },
    "Satyr": {
        "asi": {}, "flex_asi": "motm",
        "speed": "35 ft", "size": "Medium",
        "traits": ["Ram (1d6+STR bludgeoning)", "Magic Resistance (advantage on saves vs. spells)", "Mirthful Leaps (+1d8 ft to long/high jumps)", "Reveler (Persuasion & Performance proficiency)"],
        "languages": ["Common", "One of your choice"],
    },
    "Sea Elf": {
        "asi": {}, "flex_asi": "motm",
        "speed": "30 ft / 30 ft swimming", "size": "Medium",
        "traits": ["Darkvision 60 ft", "Fey Ancestry", "Trance (4-hour rest)", "Keen Senses (Perception proficiency)", "Child of the Sea (breathe water)", "Friend of the Sea (communicate with swimming beasts)"],
        "languages": ["Common", "Elvish", "One of your choice"],
    },
    "Shadar-kai": {
        "asi": {}, "flex_asi": "motm",
        "speed": "30 ft", "size": "Medium",
        "traits": ["Darkvision 60 ft", "Fey Ancestry", "Trance (4-hour rest)", "Keen Senses (Perception proficiency)", "Necrotic Resistance", "Blessing of the Raven Queen (teleport 30 ft + resist all damage until next turn, PB/lr)"],
        "languages": ["Common", "Elvish", "One of your choice"],
    },
    "Shifter": {
        "asi": {}, "flex_asi": "motm",
        "speed": "30 ft", "size": "Medium",
        "traits": ["Bestial Instincts (one skill: Acrobatics, Athletics, Intimidation, or Survival)", "Darkvision 60 ft", "Shifting (temp HP + 1-min transformation, PB/lr; subtype rider: Beasthide / Longtooth / Swiftstride / Wildhunt)"],
        "languages": ["Common", "One of your choice"],
    },
    "Tabaxi": {
        "asi": {}, "flex_asi": "motm",
        "speed": "30 ft / 20 ft climbing", "size": "Medium or Small",
        "traits": ["Cat's Claws (1d6+STR slashing; 20 ft climb speed)", "Cat's Talent (Perception & Stealth proficiency)", "Darkvision 60 ft", "Feline Agility (double speed 1/turn; reset by spending a turn with 0 movement)"],
        "languages": ["Common", "One of your choice"],
    },
    "Tortle": {
        "asi": {}, "flex_asi": "motm",
        "speed": "30 ft", "size": "Medium or Small",
        "traits": ["Claws (1d6+STR slashing)", "Hold Breath (1 hour)", "Natural Armor (AC 17 flat; no DEX bonus; can use shield)", "Shell Defense (action: +4 AC, advantage STR/CON saves, speed 0, can't react)", "Nature's Intuition (one skill: Animal Handling, Medicine, Nature, Perception, or Survival)"],
        "languages": ["Common", "One of your choice"],
    },
    "Triton": {
        "asi": {}, "flex_asi": "motm",
        "speed": "30 ft / 30 ft swimming", "size": "Medium",
        "traits": ["Amphibious (breathe air and water)", "Control Air and Water (Fog Cloud; Gust of Wind at 3rd; Water Walk at 5th; 1/lr)", "Darkvision 60 ft", "Emissary of the Sea (communicate with swimming creatures)", "Guardian of the Depths (cold resistance; ignore deep underwater drawbacks)"],
        "languages": ["Common", "One of your choice"],
    },
    "Yuan-ti": {
        "asi": {}, "flex_asi": "motm",
        "speed": "30 ft", "size": "Medium or Small",
        "traits": ["Darkvision 60 ft", "Magic Resistance (advantage on saves vs. spells and magic)", "Poison Resilience (resist poison damage; advantage vs. poisoned condition)", "Serpentine Spellcasting (Poison Spray cantrip; Animal Friendship (snakes only) at 3rd; Suggestion at 5th; 1/lr)"],
        "languages": ["Common", "One of your choice"],
    },
    "Custom Lineage": {
        "asi": {}, "flex_asi": "custom",
        "speed": "30 ft", "size": "Small or Medium",
        "traits": ["+2 to one ability score of your choice", "One feat at Level 1 (must meet prerequisites)", "Darkvision 60 ft OR one skill proficiency (your choice)", "Extra Language"],
        "languages": ["Common", "One of your choice"],
    },
}

# ac_base / ac_type: how to compute starting AC from class equipment
#   "heavy"  → fixed base, DEX ignored
#   "medium" → base + min(DEX mod, 2)
#   "light"  → base + DEX mod
#   "unarmored_barb" → 10 + DEX + CON
#   "unarmored_monk" → 10 + DEX + WIS
#   "unarmored"      → 10 + DEX
CLASSES = {
    "Barbarian": {
        "hit_die": 12, "primary_ability": "STR",
        "saving_throws": ["STR", "CON"],
        "armor_proficiencies": ["Light", "Medium", "Shields"],
        "weapon_proficiencies": ["Simple", "Martial"],
        "skill_options": ["Animal Handling", "Athletics", "Intimidation", "Nature", "Perception", "Survival"],
        "num_skills": 2,
        "starting_equipment": ["Greataxe", "Two Handaxes", "Explorer's Pack", "4 Javelins"],
        "spellcasting": None,
        "ac_base": 10, "ac_type": "unarmored_barb",
    },
    "Bard": {
        "hit_die": 8, "primary_ability": "CHA",
        "saving_throws": ["DEX", "CHA"],
        "armor_proficiencies": ["Light"],
        "weapon_proficiencies": ["Simple", "Hand Crossbow", "Longsword", "Rapier", "Shortsword"],
        "skill_options": ["Acrobatics", "Animal Handling", "Arcana", "Athletics", "Deception", "History",
                          "Insight", "Intimidation", "Investigation", "Medicine", "Nature", "Perception",
                          "Performance", "Persuasion", "Religion", "Sleight of Hand", "Stealth", "Survival"],
        "num_skills": 3,
        "starting_equipment": ["Rapier", "Diplomat's Pack", "Lute", "Leather Armor", "Dagger"],
        "spellcasting": "CHA",
        "ac_base": 11, "ac_type": "light",
    },
    "Cleric": {
        "hit_die": 8, "primary_ability": "WIS",
        "saving_throws": ["WIS", "CHA"],
        "armor_proficiencies": ["Light", "Medium", "Shields"],
        "weapon_proficiencies": ["Simple"],
        "skill_options": ["History", "Insight", "Medicine", "Persuasion", "Religion"],
        "num_skills": 2,
        "starting_equipment": ["Mace", "Scale Mail", "Light Crossbow", "20 Bolts", "Priest's Pack", "Shield", "Holy Symbol"],
        "spellcasting": "WIS",
        "ac_base": 14, "ac_type": "medium",  # Scale Mail + Shield = 14+DEX(max2)+2
        "shield": True,
    },
    "Druid": {
        "hit_die": 8, "primary_ability": "WIS",
        "saving_throws": ["INT", "WIS"],
        "armor_proficiencies": ["Light", "Medium", "Shields (nonmetal)"],
        "weapon_proficiencies": ["Club", "Dagger", "Dart", "Javelin", "Mace", "Quarterstaff", "Scimitar", "Sickle", "Sling", "Spear"],
        "skill_options": ["Arcana", "Animal Handling", "Insight", "Medicine", "Nature", "Perception", "Religion", "Survival"],
        "num_skills": 2,
        "starting_equipment": ["Wooden Shield", "Scimitar", "Leather Armor", "Explorer's Pack", "Druidic Focus"],
        "spellcasting": "WIS",
        "ac_base": 11, "ac_type": "light",  # Leather + Shield
        "shield": True,
    },
    "Fighter": {
        "hit_die": 10, "primary_ability": "STR or DEX",
        "saving_throws": ["STR", "CON"],
        "armor_proficiencies": ["All Armor", "Shields"],
        "weapon_proficiencies": ["Simple", "Martial"],
        "skill_options": ["Acrobatics", "Animal Handling", "Athletics", "History", "Insight", "Intimidation", "Perception", "Survival"],
        "num_skills": 2,
        "starting_equipment": ["Chain Mail", "Longsword", "Shield", "Light Crossbow", "20 Bolts", "Dungeoneer's Pack"],
        "spellcasting": None,
        "ac_base": 16, "ac_type": "heavy",  # Chain Mail + Shield
        "shield": True,
    },
    "Monk": {
        "hit_die": 8, "primary_ability": "DEX & WIS",
        "saving_throws": ["STR", "DEX"],
        "armor_proficiencies": [],
        "weapon_proficiencies": ["Simple", "Shortswords"],
        "skill_options": ["Acrobatics", "Athletics", "History", "Insight", "Religion", "Stealth"],
        "num_skills": 2,
        "starting_equipment": ["Shortsword", "Dungeoneer's Pack", "10 Darts"],
        "spellcasting": None,
        "ac_base": 10, "ac_type": "unarmored_monk",
    },
    "Paladin": {
        "hit_die": 10, "primary_ability": "STR & CHA",
        "saving_throws": ["WIS", "CHA"],
        "armor_proficiencies": ["All Armor", "Shields"],
        "weapon_proficiencies": ["Simple", "Martial"],
        "skill_options": ["Athletics", "Insight", "Intimidation", "Medicine", "Persuasion", "Religion"],
        "num_skills": 2,
        "starting_equipment": ["Chain Mail", "Longsword", "Shield", "Holy Symbol", "Priest's Pack", "5 Javelins"],
        "spellcasting": "CHA",
        "ac_base": 16, "ac_type": "heavy",
        "shield": True,
    },
    "Ranger": {
        "hit_die": 10, "primary_ability": "DEX & WIS",
        "saving_throws": ["STR", "DEX"],
        "armor_proficiencies": ["Light", "Medium", "Shields"],
        "weapon_proficiencies": ["Simple", "Martial"],
        "skill_options": ["Animal Handling", "Athletics", "Insight", "Investigation", "Nature", "Perception", "Stealth", "Survival"],
        "num_skills": 3,
        "starting_equipment": ["Scale Mail", "Two Shortswords", "Explorer's Pack", "Longbow", "20 Arrows"],
        "spellcasting": "WIS",
        "ac_base": 14, "ac_type": "medium",
    },
    "Rogue": {
        "hit_die": 8, "primary_ability": "DEX",
        "saving_throws": ["DEX", "INT"],
        "armor_proficiencies": ["Light"],
        "weapon_proficiencies": ["Simple", "Hand Crossbow", "Longsword", "Rapier", "Shortsword"],
        "skill_options": ["Acrobatics", "Athletics", "Deception", "Insight", "Intimidation", "Investigation",
                          "Perception", "Performance", "Persuasion", "Sleight of Hand", "Stealth"],
        "num_skills": 4,
        "starting_equipment": ["Rapier", "Shortbow", "20 Arrows", "Burglar's Pack", "Leather Armor", "Two Daggers", "Thieves' Tools"],
        "spellcasting": None,
        "ac_base": 11, "ac_type": "light",
    },
    "Sorcerer": {
        "hit_die": 6, "primary_ability": "CHA",
        "saving_throws": ["CON", "CHA"],
        "armor_proficiencies": [],
        "weapon_proficiencies": ["Dagger", "Dart", "Sling", "Quarterstaff", "Light Crossbow"],
        "skill_options": ["Arcana", "Deception", "Insight", "Intimidation", "Persuasion", "Religion"],
        "num_skills": 2,
        "starting_equipment": ["Light Crossbow", "20 Bolts", "Arcane Focus", "Explorer's Pack", "Two Daggers"],
        "spellcasting": "CHA",
        "ac_base": 10, "ac_type": "unarmored",
    },
    "Warlock": {
        "hit_die": 8, "primary_ability": "CHA",
        "saving_throws": ["WIS", "CHA"],
        "armor_proficiencies": ["Light"],
        "weapon_proficiencies": ["Simple"],
        "skill_options": ["Arcana", "Deception", "History", "Intimidation", "Investigation", "Nature", "Religion"],
        "num_skills": 2,
        "starting_equipment": ["Light Crossbow", "20 Bolts", "Arcane Focus", "Scholar's Pack", "Leather Armor", "Two Daggers"],
        "spellcasting": "CHA",
        "ac_base": 11, "ac_type": "light",
    },
    "Wizard": {
        "hit_die": 6, "primary_ability": "INT",
        "saving_throws": ["INT", "WIS"],
        "armor_proficiencies": [],
        "weapon_proficiencies": ["Dagger", "Dart", "Sling", "Quarterstaff", "Light Crossbow"],
        "skill_options": ["Arcana", "History", "Insight", "Investigation", "Medicine", "Religion"],
        "num_skills": 2,
        "starting_equipment": ["Quarterstaff", "Arcane Focus", "Scholar's Pack", "Spellbook"],
        "spellcasting": "INT",
        "ac_base": 10, "ac_type": "unarmored",
    },
}

BACKGROUNDS = {
    "Acolyte": {
        "skills": ["Insight", "Religion"],
        "equipment": ["Holy Symbol", "Prayer Book", "5 Sticks of Incense", "Vestments", "Common Clothes", "15 gp"],
        "feature": "Shelter of the Faithful",
    },
    "Charlatan": {
        "skills": ["Deception", "Sleight of Hand"],
        "equipment": ["Fine Clothes", "Disguise Kit", "Con Tools", "15 gp"],
        "feature": "False Identity",
    },
    "Criminal": {
        "skills": ["Deception", "Stealth"],
        "equipment": ["Crowbar", "Dark Common Clothes with Hood", "15 gp"],
        "feature": "Criminal Contact",
    },
    "Entertainer": {
        "skills": ["Acrobatics", "Performance"],
        "equipment": ["Musical Instrument", "Admirer's Love Letter", "Costume", "15 gp"],
        "feature": "By Popular Demand",
    },
    "Folk Hero": {
        "skills": ["Animal Handling", "Survival"],
        "equipment": ["Artisan's Tools", "Shovel", "Iron Pot", "Common Clothes", "10 gp"],
        "feature": "Rustic Hospitality",
    },
    "Guild Artisan": {
        "skills": ["Insight", "Persuasion"],
        "equipment": ["Artisan's Tools", "Letter of Introduction", "Traveler's Clothes", "15 gp"],
        "feature": "Guild Membership",
    },
    "Hermit": {
        "skills": ["Medicine", "Religion"],
        "equipment": ["Scroll Case with Notes", "Winter Blanket", "Common Clothes", "Herbalism Kit", "5 gp"],
        "feature": "Discovery",
    },
    "Noble": {
        "skills": ["History", "Persuasion"],
        "equipment": ["Fine Clothes", "Signet Ring", "Scroll of Pedigree", "25 gp"],
        "feature": "Position of Privilege",
    },
    "Outlander": {
        "skills": ["Athletics", "Survival"],
        "equipment": ["Staff", "Hunting Trap", "Trophy from Animal", "Traveler's Clothes", "10 gp"],
        "feature": "Wanderer",
    },
    "Sage": {
        "skills": ["Arcana", "History"],
        "equipment": ["Bottle of Black Ink", "Quill", "Small Knife", "Letter from Dead Colleague", "Common Clothes", "10 gp"],
        "feature": "Researcher",
    },
    "Sailor": {
        "skills": ["Athletics", "Perception"],
        "equipment": ["Belaying Pin", "50 ft Silk Rope", "Lucky Charm", "Common Clothes", "10 gp"],
        "feature": "Ship's Passage",
    },
    "Soldier": {
        "skills": ["Athletics", "Intimidation"],
        "equipment": ["Insignia of Rank", "Trophy from Enemy", "Playing Card Set", "Common Clothes", "10 gp"],
        "feature": "Military Rank",
    },
}

# ── Spell Slot Progression ────────────────────────────────────────────────────
# SPELL_SLOTS[caster_type][character_level] = {slot_level: count, ...}

SPELL_SLOTS = {
    'full': {          # Bard, Cleric, Druid, Sorcerer, Wizard
        1:  {1: 2},
        2:  {1: 3},
        3:  {1: 4, 2: 2},
        4:  {1: 4, 2: 3},
        5:  {1: 4, 2: 3, 3: 2},
        6:  {1: 4, 2: 3, 3: 3},
        7:  {1: 4, 2: 3, 3: 3, 4: 1},
        8:  {1: 4, 2: 3, 3: 3, 4: 2},
        9:  {1: 4, 2: 3, 3: 3, 4: 3, 5: 1},
        10: {1: 4, 2: 3, 3: 3, 4: 3, 5: 2},
    },
    'half': {          # Paladin, Ranger (no slots at level 1)
        1:  {},
        2:  {1: 2},
        3:  {1: 3},
        4:  {1: 3},
        5:  {1: 4, 2: 2},
        6:  {1: 4, 2: 2},
        7:  {1: 4, 2: 3},
        8:  {1: 4, 2: 3},
        9:  {1: 4, 2: 3, 3: 2},
        10: {1: 4, 2: 3, 3: 2},
    },
    'warlock': {       # Pact Magic — short rest recovery
        1:  {1: 1},
        2:  {1: 2},
        3:  {2: 2},
        4:  {2: 2},
        5:  {3: 2},
        6:  {3: 2},
        7:  {4: 2},
        8:  {4: 2},
        9:  {5: 2},
        10: {5: 2},
    },
}

SPELLCASTING_TYPE = {
    'Bard':     'full',
    'Cleric':   'full',
    'Druid':    'full',
    'Sorcerer': 'full',
    'Wizard':   'full',
    'Paladin':  'half',
    'Ranger':   'half',
    'Warlock':  'warlock',
}


# Subclasses by class. Each entry: {"name": str, "source": str, "description": str}
# source: "PHB", "XGtE", or "TCoE"
# Clerics, Sorcerers, and Warlocks choose at Level 1; all others at Level 3.
SUBCLASSES = {
    "Barbarian": [
        {"name": "Berserker",            "source": "PHB",  "description": "Goes into a frenzied rage for extra attacks; takes exhaustion to power through. Pure damage amplification at a resource cost."},
        {"name": "Totem Warrior",        "source": "PHB",  "description": "Channels the spirit of an animal totem (Bear, Eagle, Wolf, Elk, Tiger) for utility and protection. Bear totem resistance is one of the strongest defensive features in the game."},
        {"name": "Ancestral Guardian",   "source": "XGtE", "description": "Summons ancestor spirits to protect allies. Melee attackers targeting your allies have disadvantage and deal less damage; Spirit Shield reduces damage as a reaction."},
        {"name": "Storm Herald",         "source": "XGtE", "description": "Projects a damage aura while raging (cold, lightning, or thunder). AoE-focused but action-economy heavy since the aura must be reactivated each turn."},
        {"name": "Zealot",               "source": "XGtE", "description": "Divine fury deals extra radiant/necrotic damage; allies can revive you for free during a rage. Death becomes nearly irrelevant with the level-14 feature."},
        {"name": "Beast",                "source": "TCoE", "description": "Manifests natural weapons (bite, claws, or tail) while raging. Extremely action-efficient — claws give an extra bonus action attack; the tail reacts to incoming hits."},
        {"name": "Wild Magic",           "source": "TCoE", "description": "Triggers random magical surges while raging (teleport, temp HP, force damage, invisibility, etc.). Chaotic but full of upside; Bolstering Magic lets you boost allies between rages."},
    ],
    "Bard": [
        {"name": "College of Lore",      "source": "PHB",  "description": "Extra skills, Cutting Words (subtract d6 from enemy rolls), and bonus spells from any class list. The generalist support and debuff bard."},
        {"name": "College of Valor",     "source": "PHB",  "description": "Medium armor and shields, martial weapons, Combat Inspiration (add d6 to damage or AC). Turns the bard into a frontline fighter-support hybrid."},
        {"name": "College of Glamour",   "source": "XGtE", "description": "Mantle of Inspiration gives multiple allies temp HP and free movement as a bonus action. Enthralling Performance charms a crowd without concentration."},
        {"name": "College of Swords",    "source": "XGtE", "description": "Melee-focused bard with Blade Flourishes that spend Bardic Inspiration to add damage, deflect damage, or shove on a hit. Works well with two-weapon fighting or a rapier."},
        {"name": "College of Whispers",  "source": "XGtE", "description": "Psychic Blades spend Bardic Inspiration to deal extra psychic damage and steal a creature's identity after killing them. Infiltration and assassination fantasy."},
        {"name": "College of Creation",  "source": "TCoE", "description": "Note of Potential makes Bardic Inspiration dice roll with bonus effects; Mote of Potential animates an object. Excellent party utility and battlefield control."},
        {"name": "College of Eloquence", "source": "TCoE", "description": "Silver Tongue means Persuasion and Deception rolls of 9 or lower become 10. Unfailing Inspiration lets the target keep the die even on a failed roll. The strongest face and Bardic Inspiration subclass."},
    ],
    "Cleric": [
        {"name": "Knowledge Domain",     "source": "PHB",  "description": "Extra languages, tool expertise, and access to Arcana/History/Nature/Religion as domain skills. Channel Divinity reads minds or temporarily copies a creature's skills."},
        {"name": "Life Domain",          "source": "PHB",  "description": "Disciple of Life makes healing spells restore 2 + spell level extra HP. Heavy armor proficiency. The premier healing subclass."},
        {"name": "Light Domain",         "source": "PHB",  "description": "Warding Flare imposes disadvantage on incoming attacks as a reaction. Radiance of the Dawn deals AoE radiant damage. Offense- and protection-focused divine caster."},
        {"name": "Nature Domain",        "source": "PHB",  "description": "Heavy armor and a druid cantrip; Charm Animals and Plants is a powerful Channel Divinity. Resistant to a chosen damage type at level 6."},
        {"name": "Tempest Domain",       "source": "PHB",  "description": "Heavy armor, martial weapons, Thunderbolt Strike pushes enemies on lightning/thunder damage, and Destructive Wrath maximizes a lightning or thunder spell once per rest."},
        {"name": "Trickery Domain",      "source": "PHB",  "description": "Duplicate self (Invoke Duplicity) and cast through the copy. Gets Blink, Dimension Door, and Modify Memory. Best for concentration spells and misdirection."},
        {"name": "War Domain",           "source": "PHB",  "description": "Extra Attack at level 6, War Priest gives bonus action weapon attacks using Wisdom modifier per rest. Heavy armor and martial weapons. High-damage melee cleric."},
        {"name": "Forge Domain",         "source": "XGtE", "description": "Blessing of the Forge enchants a weapon or armor daily (+1 bonus). Heavy armor, and Soul of the Forge adds +1 AC in heavy armor. Best armor in the game for a Cleric."},
        {"name": "Grave Domain",         "source": "XGtE", "description": "Eyes of the Grave detects undead; Sentinel at Death's Door cancels critical hits on allies as a reaction. Healer-protector focused on fighting death itself."},
        {"name": "Order Domain",         "source": "TCoE", "description": "Voice of Authority lets an ally make a weapon attack as a reaction when you cast a spell on them. Heavy armor. The commander cleric — buffs allies while keeping pressure up."},
        {"name": "Peace Domain",         "source": "TCoE", "description": "Emboldening Bond links allies to share d4 bonuses on attacks, saves, and checks. Protective Bond lets them teleport to absorb damage for each other. Exceptional party support."},
        {"name": "Twilight Domain",      "source": "TCoE", "description": "Twilight Sanctuary gives temp HP or ends charmed/frightened to all allies in a radius each turn. Darkvision aura for the whole party. Considered one of the strongest Cleric subclasses."},
    ],
    "Druid": [
        {"name": "Circle of the Land",   "source": "PHB",  "description": "Extra cantrip, bonus spell recovery on short rest, and terrain-based bonus spells (Arctic, Coast, Desert, Forest, Grassland, Mountain, Swamp, Underdark). The spellcaster-focused druid."},
        {"name": "Circle of the Moon",   "source": "PHB",  "description": "Wild Shape into CR 1 beasts at level 2 (scales to CR 6 at level 6), can Wild Shape into elementals. Dramatically more powerful combat Wild Shapes than base Druid."},
        {"name": "Circle of Dreams",     "source": "XGtE", "description": "Balm of the Summer Court heals allies using a pool of d6s recharged on long rest. Hearth of Moonlight and Shadow makes short rests in the wild safer."},
        {"name": "Circle of the Shepherd","source": "XGtE","description": "Spirit Totem summons an aura that gives party advantage on checks, temp HP, or regain HP. Supercharges conjuration spells (doubled summoned creature HP). Best conjurer subclass."},
        {"name": "Circle of Spores",     "source": "TCoE", "description": "Halo of Spores deals necrotic damage as a reaction; Symbiotic Entity uses Wild Shape charges to gain temp HP and add 1d6 necrotic to melee attacks. A melee-capable druid without transforming."},
        {"name": "Circle of Stars",      "source": "TCoE", "description": "Starry Form gives three constellations (Archer for ranged radiant bonus action, Chalice for healing bonuses, Dragon for concentration advantage). Strong sustained utility across the day."},
        {"name": "Circle of Wildfire",   "source": "TCoE", "description": "Summons a Wildfire Spirit (similar to Find Familiar) that teleports allies, deals fire damage in an AoE, and revives you once per day. Offense and party repositioning."},
    ],
    "Fighter": [
        {"name": "Champion",             "source": "PHB",  "description": "Improved Critical (crit on 19-20 at level 3, 18-20 at level 15) and passive bonuses like extra fighting styles and remarkable athlete. The simple, no-resource melee powerhouse."},
        {"name": "Battle Master",        "source": "PHB",  "description": "Maneuvers (superiority dice) add tactical effects to attacks: trip, disarm, feint, rally, riposte, etc. The most flexible and mechanically interesting fighter subclass."},
        {"name": "Eldritch Knight",      "source": "PHB",  "description": "Gains Wizard spellcasting (abjuration and evocation focused), can bond weapons to return them on command, and eventually cast spells as a bonus action on attack turns."},
        {"name": "Arcane Archer",        "source": "XGtE", "description": "Two Arcane Shot uses per rest that add special effects to arrows (banishing, bursting, entangling, etc.). Ranged-only; limited uses are the main drawback."},
        {"name": "Cavalier",             "source": "XGtE", "description": "Marks a target forcing them to attack you or take disadvantage; Unwavering Mark lets you make a bonus action attack when the marked creature attacks an ally. The mounted and defender fighter."},
        {"name": "Samurai",              "source": "XGtE", "description": "Fighting Spirit grants advantage on attacks and temp HP as a bonus action (3/long rest). Elegant Courtier adds WIS to Persuasion. Reliable damage output and surprising social utility."},
        {"name": "Psi Warrior",          "source": "TCoE", "description": "Psionic dice (d6s) power telekinetic pushes, damage reduction, and movement boosts. A short-rest-recharging resource pool adding force damage and battlefield manipulation to attacks."},
        {"name": "Rune Knight",          "source": "TCoE", "description": "Inscribes magical runes on equipment (Cloud for Advantage on checks, Fire for extra damage, Frost for Armor of Agathys, etc.) and can grow to Large size. Strong and thematically flavorful."},
    ],
    "Monk": [
        {"name": "Way of the Open Hand", "source": "PHB",  "description": "Open Hand Technique adds free effects to Flurry of Blows (prone, push, or deny reactions). Wholeness of Body heals yourself 3× monk level once per long rest. The purist striking monk."},
        {"name": "Way of Shadow",        "source": "PHB",  "description": "Casts darkness, darkvision, pass without trace, and silence for free (ki points). Shadow Step teleports 60 ft between dim light/darkness as a bonus action."},
        {"name": "Way of the Four Elements","source":"PHB","description": "Spends ki to cast a limited list of elemental spells (burning hands, water whip, wall of fire, etc.). Ki-hungry; the elemental effects are impressive but expensive."},
        {"name": "Way of the Drunken Master","source":"XGtE","description": "Drunken Technique adds Disengage and +10 ft speed to Flurry of Blows. Tipsy Sway redirects missed attacks to adjacent creatures. Slippery battlefield controller."},
        {"name": "Way of the Kensei",    "source": "XGtE", "description": "Designates specific weapons as Kensei weapons (proficient, count as monk weapons). Adds damage to ranged attacks and extra AC when using Kensei weapons. The weapon-master monk."},
        {"name": "Way of the Sun Soul",  "source": "XGtE", "description": "Radiant Sun Bolt is a ranged ki-powered attack option replacing unarmed strikes. Searing Arc Strike and Searing Sunburst deal AoE radiant damage. Ranged and AoE-capable monk."},
        {"name": "Way of the Astral Self","source":"TCoE", "description": "Summons astral arms extending reach and dealing force damage; astral visage grants darkvision, advantage on WIS/CHA saves, and +2 to WIS/CHA checks. High-ki-cost but visually and mechanically dramatic."},
        {"name": "Way of Mercy",         "source": "TCoE", "description": "Hands of Healing uses ki to heal as a bonus action (superior action economy for a healer monk). Hands of Harm adds necrotic damage and the poisoned condition. Versatile medic-assassin."},
    ],
    "Paladin": [
        {"name": "Oath of Devotion",     "source": "PHB",  "description": "Sacred Weapon adds CHA to attack rolls; Holy Nimbus radiates damage to nearby enemies. Classic holy warrior archetype — the tank-support paladin."},
        {"name": "Oath of the Ancients", "source": "PHB",  "description": "Aura of Warding at level 7 gives all nearby allies resistance to spell damage. Nature-themed oath with strong debuff and healing spells like Ensnaring Strike and Misty Step."},
        {"name": "Oath of Vengeance",    "source": "PHB",  "description": "Vow of Enmity gives advantage on attacks against a single target; Relentless Avenger lets you move half your speed when the target moves away. Single-target lock-down and damage."},
        {"name": "Oath of Conquest",     "source": "XGtE", "description": "Conquering Presence frightens enemies; Aura of Conquest (level 7) causes frightened enemies to be paralyzed while in the aura and take psychic damage. The fear-and-domination paladin."},
        {"name": "Oath of Redemption",   "source": "XGtE", "description": "Rebuke the Violent punishes allies' attackers with radiant damage; Protective Spirit heals you at the end of your turn. Pacifist flavor with strong self-sustain and protective abilities."},
        {"name": "Oath of Glory",        "source": "TCoE", "description": "Inspiring Smite distributes temp HP to allies after a Divine Smite. Aura of Alacrity (level 7) boosts walking speed for the whole party. Mobility and morale support paladin."},
        {"name": "Oath of the Watchers", "source": "TCoE", "description": "Watcher's Will gives allies advantage on INT/WIS/CHA saves as a Channel Divinity. Mortal Bulwark gives advantage vs. aberrations, celestials, elementals, fey, and fiends at level 20."},
    ],
    "Ranger": [
        {"name": "Hunter",               "source": "PHB",  "description": "Picks Hunter's Prey (colossus slayer, giant killer, horde breaker) and Defensive Tactics (escape the horde, multiattack defense, steel will). Very flexible; chooses from a menu of upgrades."},
        {"name": "Beast Master",         "source": "PHB",  "description": "Forms a bond with a beast companion that acts on your turn. PHB version is limited; TCoE's Primal Companion is the superior version of this fantasy."},
        {"name": "Gloom Stalker",        "source": "XGtE", "description": "Invisible in darkness (even magical), extra attack on the first turn of combat, and Dread Ambusher grants extra speed and attacks on the first round. Dominant ambush and dungeon-crawl ranger."},
        {"name": "Horizon Walker",       "source": "XGtE", "description": "Detects planar portals; Planar Warrior deals force damage on one attack per turn. Ethereal Step lets you briefly blink to the Ethereal Plane. Planar-travel flavor with consistent force damage."},
        {"name": "Monster Slayer",       "source": "XGtE", "description": "Hunter's Sense reveals damage immunities/resistances. Slayer's Prey marks a target for extra d6 damage each turn. Magic-User's Nemesis can negate one spell per rest as a reaction."},
        {"name": "Fey Wanderer",         "source": "TCoE", "description": "Dreadful Strikes adds psychic damage to weapon attacks; Otherworldly Glamour adds WIS to CHA checks. Beguiling Twist passes charmed/frightened effects to other targets. Debuffer ranger."},
        {"name": "Swarmkeeper",          "source": "TCoE", "description": "A swarm of spirits surrounds you, dealing 1d6 extra damage and choosing to push, pull, or move you after each attack. Gathered Swarm scales with additional effects at higher levels."},
    ],
    "Rogue": [
        {"name": "Thief",                "source": "PHB",  "description": "Fast Hands uses the bonus action for item interactions (including magic items) and Second-Story Work adds DEX to jump distance. Simple but broadly useful."},
        {"name": "Assassin",             "source": "PHB",  "description": "Automatically crits on surprise rounds and against creatures that haven't acted yet. Infiltration Expertise creates false identities. Devastating in campaigns with ambushes and intrigue."},
        {"name": "Arcane Trickster",     "source": "PHB",  "description": "Gains Wizard cantrips and spells (illusion and enchantment focused), can deliver touch spells via Sneak Attack, and eventually steal concentration spells. The spellcaster rogue."},
        {"name": "Inquisitive",          "source": "XGtE", "description": "Ear for Deceit sets a minimum of 8 on Insight checks. Insightful Fighting lets you Sneak Attack a target without needing an ally adjacent if you win an Insight contest. Investigation and social specialist."},
        {"name": "Mastermind",           "source": "XGtE", "description": "Master of Tactics: Help as a bonus action from up to 30 ft away. Mimicry copies voices and accents. Social manipulation and long-range Sneak Attack support."},
        {"name": "Scout",                "source": "XGtE", "description": "Skirmisher moves half speed as a reaction when a creature ends its turn adjacent. Survivalist gains expertise in Nature and Survival. The wilderness and skirmisher rogue."},
        {"name": "Swashbuckler",         "source": "XGtE", "description": "Fancy Footwork lets you Disengage for free after attacking a creature. Rakish Audacity Sneak Attacks on a 1v1 without needing an ally adjacent. The duelist rogue — fastest, most mobile option."},
        {"name": "Phantom",              "source": "TCoE", "description": "Whispers of the Dead grants a random skill or tool proficiency after each rest. Wails from the Grave deals necrotic damage to a second creature after a Sneak Attack. Death-themed utility rogue."},
        {"name": "Soulknife",            "source": "TCoE", "description": "Creates psychic blades as free-action weapons (no gear needed). Psychic Whispers enables silent telepathy; Psi-Powered Leap levitates without using movement. No-equipment psionic rogue."},
    ],
    "Sorcerer": [
        {"name": "Draconic Bloodline",   "source": "PHB",  "description": "Natural armor (13+DEX, no armor needed), bonus HP per level, and affinity with a dragon's damage type (resistant, empowered spells). The tanky and damage-focused sorcerer."},
        {"name": "Wild Magic",           "source": "PHB",  "description": "Wild Magic Surge triggers random effects after casting (the DM can trigger a roll at any time). Tides of Chaos grants advantage once per rest; Bend Luck spends sorcery points to adjust any d20."},
        {"name": "Divine Soul",          "source": "XGtE", "description": "Gains access to the full Cleric spell list in addition to Sorcerer spells. Favored by the Gods adds 2d4 to a failed save or attack roll once per rest. Divine magic through sorcerer action economy."},
        {"name": "Shadow Magic",         "source": "XGtE", "description": "Superior Darkvision (120 ft), Eyes of the Dark grants free Darkness spell, Strength of the Grave forces a death save reroll when reduced to 0 HP. Dark and death-resisting sorcerer."},
        {"name": "Storm Sorcery",        "source": "XGtE", "description": "Wind Speaker grants resistance to lightning and thunder. Tempestuous Magic lets you fly 10 ft as a bonus action after casting a leveled spell. Mobile AoE sorcerer with sky-movement."},
        {"name": "Aberrant Mind",        "source": "TCoE", "description": "Telepathic Speech enables free silent communication. Psionic Spells adds psychic/divination spells (Dissonant Whispers, Detect Thoughts, Telekinesis, etc.) that can be converted using sorcery points."},
        {"name": "Clockwork Soul",       "source": "TCoE", "description": "Restore Balance cancels advantage or disadvantage on any roll in sight as a reaction. Clockwork Spells adds control spells (Alarm, Dispel Magic, Counterspell, etc.) for free. Order and anti-luck manipulation."},
    ],
    "Warlock": [
        {"name": "The Archfey",          "source": "PHB",  "description": "Fey Presence frightens or charms all creatures in a 10-ft cube. Misty Escape reacts to damage by turning invisible and teleporting 60 ft. Illusion and charm-focused patron."},
        {"name": "The Fiend",            "source": "PHB",  "description": "Dark One's Blessing gains temp HP equal to CHA mod + spell level when killing an enemy. Bonus spells include Fireball and Wall of Fire. The most damage-efficient Warlock subclass."},
        {"name": "The Great Old One",    "source": "PHB",  "description": "Telepathy with any creature within 30 ft (no language needed). Awakened Mind enables silent two-way telepathic communication. Entropic Ward reacts to a missed attack for advantage next turn."},
        {"name": "The Celestial",        "source": "XGtE", "description": "Healing Light uses a pool of d6s to heal as a bonus action. Bonus spells include Cure Wounds, Revivify, and Flame Strike. Warlock who can heal effectively without burning spell slots."},
        {"name": "The Hexblade",         "source": "XGtE", "description": "Hexblade's Curse marks a target (crit on 19+, heal on kill, bonus to attacks equal to PB). Hex Warrior makes CHA the attack/damage stat for a one-handed weapon. The melee-CHA warlock."},
        {"name": "The Fathomless",       "source": "TCoE", "description": "Tentacle of the Deeps creates a 10-ft tentacle that deals cold damage and slows. Gift of the Sea grants 40-ft swim speed and water breathing. Aquatic-themed patron with battlefield control."},
        {"name": "The Genie",            "source": "TCoE", "description": "Genie's Vessel stores and extends spell slots in a tiny extradimensional space. Elemental Gift at level 6 grants flight or resistance. Extremely versatile — genie type (Dao/Djinni/Efreeti/Marid) determines bonus spells."},
    ],
    "Wizard": [
        {"name": "School of Abjuration", "source": "PHB",  "description": "Arcane Ward absorbs damage using a HP pool recharged when casting abjuration spells. Projected Ward extends it to adjacent allies. Durable defensive wizard."},
        {"name": "School of Conjuration","source": "PHB",  "description": "Benign Transposition teleports a willing creature or yourself 30 ft once per rest. Minor Conjuration creates a small mundane object. Focused on reliable teleportation and summoning."},
        {"name": "School of Divination", "source": "PHB",  "description": "Portent: roll two d20s at the start of each day and replace any d20 roll with them (any creature, any time). Arguably the strongest early subclass feature in the game."},
        {"name": "School of Enchantment","source": "PHB",  "description": "Hypnotic Gaze sustains a charm on one creature each turn without concentration. Instinctive Charm redirects attacks against you to an adjacent creature as a reaction."},
        {"name": "School of Evocation",  "source": "PHB",  "description": "Sculpt Spells excludes up to 1+spell_level allies from AoE damage (they automatically succeed). Empowered Evocation adds INT modifier to evocation damage rolls."},
        {"name": "School of Illusion",   "source": "PHB",  "description": "Improved Minor Illusion creates both sound and image simultaneously. Malleable Illusions changes any non-instantaneous illusion spell as a bonus action. Best at making illusions interactive and persistent."},
        {"name": "School of Necromancy", "source": "PHB",  "description": "Grim Harvest regains HP equal to 2× (or 3× for necromancy) spell level when a spell kills a creature. Undead Thralls animates an extra corpse per Animate Dead with bonus max HP and attack."},
        {"name": "School of Transmutation","source":"PHB", "description": "Transmuter's Stone provides ongoing passive benefits (darkvision, extra speed, concentration advantage, or resistance). Minor Alchemy temporarily changes material composition."},
        {"name": "Bladesinger",          "source": "XGtE", "description": "Bladesong adds INT to AC and concentration saves while active, +10 speed, advantage on Acrobatics. Extra Attack at level 6. The melee-wizard, AC stacks absurdly high with mage armor + INT."},
        {"name": "War Magic",            "source": "XGtE", "description": "Arcane Deflection adds +2 AC or +4 to saving throws as a reaction after being missed/failed (restricts next spell to cantrip). Tactical Wit adds INT to initiative."},
        {"name": "Chronurgy Magic",      "source": "TCoE", "description": "Chronal Shift rerolls any d20 twice per rest (after seeing the result). Momentary Stasis incapacitates a creature for one round on a CON save. Time-manipulation specialist."},
        {"name": "Graviturgy Magic",     "source": "TCoE", "description": "Adjust Density halves or doubles a creature's weight (speed halved or jump doubled; resistance or vulnerability to bludgeoning). Gravity Well teleports a creature 5 ft after any spell targeting it."},
        {"name": "Order of Scribes",     "source": "TCoE", "description": "Awakened Spellbook lets you change a spell's damage type and use it as your spellcasting focus. Manifest Mind summons a spectral book that lets you cast touch/short-range spells at range."},
    ],
}


def get_spell_slots(class_name, level=1):
    """Return {slot_level_str: {max, current}} for the given class and character level."""
    sc_type = SPELLCASTING_TYPE.get(class_name)
    if not sc_type:
        return {}
    table = SPELL_SLOTS.get(sc_type, {})
    capped = min(level, max(table.keys()))
    return {
        str(sl): {'max': count, 'current': count}
        for sl, count in table.get(capped, {}).items()
    }
