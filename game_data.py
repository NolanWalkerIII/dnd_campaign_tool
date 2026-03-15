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
