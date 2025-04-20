# --------------------
# Save Data Constants
# --------------------

SAVE_FILE_SIZE = 128 * 1024  # 128KB
RTC_FOOTER_SIZE = 0x10  # 16 bytes
RTC_SAVE_SIZE = SAVE_FILE_SIZE + RTC_FOOTER_SIZE

SAVE_BLOCK_SIZE = 14 * 0x1000  # 14 sections of 4096 bytes each

# --------------------
# Save Section Constants
# --------------------

SAVE_SECTION_SIZE = 0x1000  # 4096 bytes
SECTION_DATA_SIZE = 0xFF0  # 4080 bytes (minus footer)
FINAL_SECTION_ID = 13

SECTION_COUNT = {"Vanilla": 14, "CFRU": 2}

CFRU_SECTIONS = [30, 31]


# --------------------
# Party Constants
# --------------------
PARTY_OFFSET = (0x38, 0x290)
PARTY_COUNT = 6
POKEMON_SIZE = 0x64  # 100 bytes per Pokémon in party

# --------------------
# Box Constants
# --------------------

BOXMON_SIZE = 0x3A  # 58 bytes per Pokémon in box
FRLG_BOXES = 19
MONS_PER_BOX = 30
BOX_COUNT = 25
BOX_MON_TOTAL = BOX_COUNT * MONS_PER_BOX

BOX_OFFSETS = {
    0: (0xB0, 0x77C),
    2: (0xF18, 0xFF0),
    3: (0x0, 0xCC0),
    5: (0x4, 0xFF0),
    6: (0x0, 0xFF0),
    7: (0x0, 0xFF0),
    8: (0x0, 0xFF0),
    9: (0x0, 0xFF0),
    10: (0x0, 0xFF0),
    11: (0x0, 0xFF0),
    12: (0x0, 0xFF0),
    13: (0x0, 0x1A8),
    30: (0xB0C, 0xFF0),
    31: (0x0, 0xF80),
}

# This order is important too, but it's intuitive
FRLG_BOX_SECTIONS = [5, 6, 7, 8, 9, 10, 11, 12, 13]

CFRU_BOX_SECTIONS = [30, 31, 2, 3, 0]  # THIS ORDER IS IMPORTANT


# --------------------
# Section Offsets
# --------------------
SECTION_ID_OFFSET = (0xFF4, 0xFF6)
CHECKSUM_OFFSET = (0xFF6, 0xFF8)
SAVE_INDEX_OFFSET = (0xFFC, 0x1000)

# --------------------
# Section IDs
# --------------------

S_IDS = {
    "Party": 1,
}


# --------------------
# Raw Byte Types
# --------------------

BYTE_TYPES = {
    "u8": (0, 1),
    "u16": (0, 2),
    "u32": (0, 4),
    "s8": (0, 1),
    "s16": (0, 2),
    "s32": (0, 4),
    "bool": (0, 1),
}

# --------------------
# Pokemon Constants
# --------------------

POKEMON_OFFSETS = {
    "personal_id": (0x0, 0x4),  # (0, 4)
    "nickname": (0x8, 0x12),  # (8, 18)
    "species": (0x20, 0x22),  # (32, 34)
    "held_item_id": (0x22, 0x24),  # (34, 36)
    "evs": (0x38, 0x3E),  # (56, 62) - 6 bytes for 6 individual EV values
    # Bit packed IVs + 2 flags (is_egg, has_hidden_ability)
    "ivs_data": (0x48, 0x4C),  # (72, 76)
    "moves": (0x2C, 0x34),  # (44, 52) - 4 moves × 2 bytes each = 8 bytes
    "level": (0x54, 0x55),  # (84, 85)
}

BOXMON_OFFSETS = {
    "personal_id": (0x0, 0x4),  # (0, 4)
    "nickname": (0x8, 0x12),  # (8, 18)
    "species": (0x1C, 0x1E),  # (28, 30)
    "held_item_id": (0x1E, 0x20),  # (30, 32)
    "xp": (0x20, 0x24),  # (32, 36)
    "moves": (0x27, 0x2C),  # (39, 44)
    "evs": (0x2C, 0x32),  # (44, 50)
    "ivs_data": (0x36, 0x3A),  # (54, 58)
}


NATURES = {
    0: "Hardy",
    1: "Lonely",
    2: "Brave",
    3: "Adamant",
    4: "Naughty",
    5: "Bold",
    6: "Docile",
    7: "Relaxed",
    8: "Impish",
    9: "Lax",
    10: "Timid",
    11: "Hasty",
    12: "Serious",
    13: "Jolly",
    14: "Naive",
    15: "Modest",
    16: "Mild",
    17: "Quiet",
    18: "Bashful",
    19: "Rash",
    20: "Calm",
    21: "Gentle",
    22: "Sassy",
    23: "Careful",
    24: "Quirky",
}

# --------------------
# Character Mapping
# --------------------

CHARACTER_MAP = {
    0x00: " ",
    0x01: "À",
    0x02: "Á",
    0x03: "Â",
    0x04: "Ç",
    0x05: "È",
    0x06: "É",
    0x07: "Ê",
    0x08: "Ë",
    0x09: "Ì",
    0x0A: " ",
    0x0B: "Î",
    0x0C: "Ï",
    0x0D: "Ò",
    0x0E: "Ó",
    0x0F: "Ô",
    0x10: "Œ",
    0x11: "Ù",
    0x12: "Ú",
    0x13: "Û",
    0x14: "Ñ",
    0x15: "ß",
    0x16: "à",
    0x17: "á",
    0x18: " ",
    0x19: "ç",
    0x1A: "é",
    0x1B: "ê",
    0x1C: "ë",
    0x1D: "ì",
    0x1E: "í",
    0x1F: " ",
    0x20: "ï",
    0x21: "ò",
    0x22: "ó",
    0x23: "ô",
    0x24: "œ",
    0x25: "ù",
    0x26: "ú",
    0x27: "û",
    0x28: "",
    0x29: "ñ",
    0x2A: "ª",
    0x2B: "º",
    0x2C: "ᵉʳ",
    0x2D: "&",
    0x2E: "+",
    0x2F: "=",
    0x30: ";",
    0x31: "¿",
    0x32: "¡",
    0x33: "Pk",
    0x34: "Mn",
    0x35: "Po",
    0x36: "ké",
    0x37: "Í",
    0x38: "%",
    0x39: "(",
    0x3A: ")",
    0x3B: "▾",
    0x3C: "▸",
    0x3D: "▹",
    0x3E: "♀",
    0x3F: "♂",
    0x40: " ",
    0x41: " ",
    0x42: " ",
    0x43: " ",
    0x44: " ",
    0x45: " ",
    0x46: " ",
    0x47: " ",
    0x48: " ",
    0x49: " ",
    0x4A: " ",
    0x4B: " ",
    0x4C: " ",
    0x4D: " ",
    0x4E: " ",
    0x4F: " ",
    0x50: " ",
    0x51: " ",
    0x52: " ",
    0x53: " ",
    0x54: " ",
    0x55: " ",
    0x56: " ",
    0x57: " ",
    0x58: " ",
    0x59: " ",
    0x5A: " ",
    0x5B: " ",
    0x5C: " ",
    0x5D: " ",
    0x5E: " ",
    0x5F: " ",
    0x60: " ",
    0x61: " ",
    0x62: " ",
    0x63: " ",
    0x64: " ",
    0x65: " ",
    0x66: " ",
    0x67: " ",
    0x68: " ",
    0x69: " ",
    0x6A: " ",
    0x6B: " ",
    0x6C: " ",
    0x6D: " ",
    0x6E: " ",
    0x6F: " ",
    0x70: " ",
    0x71: " ",
    0x72: " ",
    0x73: " ",
    0x74: " ",
    0x75: " ",
    0x76: " ",
    0x77: " ",
    0x78: " ",
    0x79: " ",
    0x7A: " ",
    0x7B: " ",
    0x7C: " ",
    0x7D: " ",
    0x7E: " ",
    0x7F: " ",
    0x80: "0",
    0x81: "1",
    0x82: "2",
    0x83: "3",
    0x84: "4",
    0x85: "5",
    0x86: "6",
    0x87: "7",
    0x88: "8",
    0x89: "9",
    0x8A: "!",
    0x8B: "?",
    0x8C: ".",
    0x8D: "-",
    0x8E: "·",
    0x8F: "…",
    0x90: "“",
    0x91: "”",
    0x92: " ",
    0x93: " ",
    0x94: "♂",
    0x95: "♀",
    0x96: "$",
    0x97: ",",
    0x98: " ",
    0x99: "÷",
    0x9A: " ",
    0x9B: " ",
    0x9C: " ",
    0x9D: " ",
    0x9E: " ",
    0x9F: " ",
    0xA0: "ʳᵉ",
    0xA1: "0",
    0xA2: "1",
    0xA3: "2",
    0xA4: "3",
    0xA5: "4",
    0xA6: "5",
    0xA7: "6",
    0xA8: "7",
    0xA9: "8",
    0xAA: "9",
    0xAB: "!",
    0xAC: "?",
    0xAD: ".",
    0xAE: "-",
    0xAF: "･",
    0xB0: "‥",
    0xB1: "“",
    0xB2: "”",
    0xB3: "‘",
    0xB4: "'",
    0xB5: "♂",
    0xB6: "♀",
    0xB7: "$",
    0xB8: ",",
    0xB9: "×",
    0xBA: "/",
    0xBB: "A",
    0xBC: "B",
    0xBD: "C",
    0xBE: "D",
    0xBF: "E",
    0xC0: "F",
    0xC1: "G",
    0xC2: "H",
    0xC3: "I",
    0xC4: "J",
    0xC5: "K",
    0xC6: "L",
    0xC7: "M",
    0xC8: "N",
    0xC9: "O",
    0xCA: "P",
    0xCB: "Q",
    0xCC: "R",
    0xCD: "S",
    0xCE: "T",
    0xCF: "U",
    0xD0: "V",
    0xD1: "W",
    0xD2: "X",
    0xD3: "Y",
    0xD4: "Z",
    0xD5: "a",
    0xD6: "b",
    0xD7: "c",
    0xD8: "d",
    0xD9: "e",
    0xDA: "f",
    0xDB: "g",
    0xDC: "h",
    0xDD: "i",
    0xDE: "j",
    0xDF: "k",
    0xE0: "l",
    0xE1: "m",
    0xE2: "n",
    0xE3: "o",
    0xE4: "p",
    0xE5: "q",
    0xE6: "r",
    0xE7: "s",
    0xE8: "t",
    0xE9: "u",
    0xEA: "v",
    0xEB: "w",
    0xEC: "x",
    0xED: "y",
    0xEE: "z",
    0xEF: "►",
    0xF0: ":",
    0xF1: "Ä",
    0xF2: "Ö",
    0xF3: "Ü",
    0xF4: "ä",
    0xF5: "ö",
    0xF6: "ü",
    0xF7: " ",
    0xF8: " ",
    0xF9: " ",
    0xFA: " ",
    0xFB: " ",
    0xFC: " ",
    0xFD: " ",
    0xFE: " ",
    0xFF: "",
}
