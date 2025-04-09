import math
from constants import CHARACTER_MAP, POKEMON_OFFSETS, NATURES, BOXMON_OFFSETS


def decode_gba_string(data: list[int]) -> str:
    chars = []
    for b in data:
        if b == 0xFF:
            break
        chars.append(CHARACTER_MAP.get(b, "?"))  # fallback for unknown bytes
    return "".join(chars)


def extract_raw_field(section, field_name, type=0):
    """
    Extracts a specific field from a section using predefined offsets.
    Args:
        section (bytes): The section data from which the field is to be extracted.
        field_name (str): The name of the field to extract.
    Returns:
        int: The extracted field value as an integer.
    Raises:
        KeyError: If the field_name is not found in SECTION_OFFSETS.
    """
    if type not in (0, 1):
        raise ValueError("Type must be 0 (Pokemon) or 1 (Boxmon)")

    chosen_offsets = POKEMON_OFFSETS if type == 0 else BOXMON_OFFSETS

    if field_name not in chosen_offsets:
        raise KeyError(f"Field '{field_name}' not found in POKEMON_OFFSETS")

    start, size = chosen_offsets[field_name]
    stop = start + size
    raw_bytes = section[start:stop]
    return raw_bytes


def extract_poke_field(section, field_name, type=0):
    """
    Extracts a specific field from a section using predefined offsets.
    Args:
        section (bytes): The section data from which the field is to be extracted.
        field_name (str): The name of the field to extract.
    Returns:
        int: The extracted field value as an integer.
    Raises:
        KeyError: If the field_name is not found in SECTION_OFFSETS.
    """
    if type not in (0, 1):
        raise ValueError("Type must be 0 (Pokemon) or 1 (Boxmon)")

    chosen_offsets = POKEMON_OFFSETS if type == 0 else BOXMON_OFFSETS

    if field_name not in chosen_offsets:
        raise KeyError(f"Field '{field_name}' not found in POKEMON_OFFSETS")

    start, size = chosen_offsets[field_name]
    stop = start + size
    raw_bytes = section[start:stop]
    return int.from_bytes(raw_bytes, byteorder="little")


def extract_multi_field(section, field_name, count, element_size=2, type=0):
    """
    Extracts a list of integers from a multi-value field.
    Args:
        section (bytes): The raw data.
        field_name (str): Key from POKEMON_OFFSETS.
        count (int): How many elements to extract.
        element_size (int): Size in bytes of each element (default 2 for 16-bit values).
    Returns:
        list[int]: List of extracted values.
    """
    if type not in (0, 1):
        raise ValueError("Type must be 0 (Pokemon) or 1 (Boxmon)")

    chosen_offsets = POKEMON_OFFSETS if type == 0 else BOXMON_OFFSETS

    if field_name not in chosen_offsets:
        raise KeyError(f"Field '{field_name}' not found in POKEMON_OFFSETS")

    start, total_size = chosen_offsets[field_name]
    stop = start + total_size
    raw_bytes = section[start:stop]

    return [
        int.from_bytes(raw_bytes[i : i + element_size], byteorder="little")
        for i in range(0, count * element_size, element_size)
    ]


def calculate_nature(personal_id: int) -> str:
    """
    Calculate the nature based on the personal ID.
    Args:
        personal_id (int): The personal ID of the Pokémon.
    Returns:
        str: The nature name.
    """
    return NATURES[personal_id % 25]


def unpack_ivs(ivs_data):
    """
    Extracts the 6 IV values from a packed 32-bit integer.
    Returns: [iv_hp, iv_attack, iv_defense, iv_speed, iv_special_attack, iv_special_defense]
    """
    return [
        (ivs_data >> 0) & 0x1F,
        (ivs_data >> 5) & 0x1F,
        (ivs_data >> 10) & 0x1F,
        (ivs_data >> 15) & 0x1F,
        (ivs_data >> 20) & 0x1F,
        (ivs_data >> 25) & 0x1F,
    ]


def is_egg(ivs_data):
    """Returns True if the Pokémon is an Egg, based on bit 30."""
    return bool((ivs_data >> 30) & 0x01)


def has_hidden_ability(ivs_data):
    """Returns True if the Pokémon has a hidden ability, based on bit 31."""
    return bool((ivs_data >> 31) & 0x01)


def unpack_moves(move_bytes):
    """
    Extracts moves from a packed 5 byte value
    """
    val = int.from_bytes(move_bytes, "little")
    return [(val >> (10 * i)) & 0x3FF for i in range(4)]


def exp_required(level, growth_rate):
    if growth_rate == "fast":
        return (4 * level**3) // 5
    elif growth_rate in ("medium", "medium-fast"):
        return level**3
    elif growth_rate == "medium-slow":
        return (6 * level**3) // 5 - 15 * level**2 + 100 * level - 140
    elif growth_rate == "slow":
        return (5 * level**3) // 4
    elif growth_rate == "erratic":
        if level <= 50:
            return (level**3 * (100 - level)) // 50
        elif level <= 68:
            return (level**3 * (150 - level)) // 100
        elif level <= 97:
            return (level**3 * ((1911 - 10 * level) // 3)) // 500
        else:
            return (level**3 * (160 - level)) // 100
    elif growth_rate == "fluctuating":
        if level <= 15:
            return math.floor(level**3 * (((level + 1) / 3 + 24) / 50))
        elif level <= 35:
            return math.floor(level**3 * ((level + 14) / 50))
        else:
            return math.floor(level**3 * ((level / 2 + 32) / 50))
    else:
        raise ValueError(f"Unsupported growth rate: {growth_rate}")


def xp_to_lvl(xp, growth_rate):
    low = 1
    high = 100

    while low < high:
        mid = (low + high + 1) // 2
        if exp_required(mid, growth_rate) <= xp:
            low = mid
        else:
            high = mid - 1

    return low
