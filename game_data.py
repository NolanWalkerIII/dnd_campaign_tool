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
