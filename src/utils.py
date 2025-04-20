import math
from constants import CHARACTER_MAP, NATURES


def get_slice(raw_bytes: bytes, byte_range: tuple) -> bytes:
    start, stop = byte_range
    return raw_bytes[start:stop]


def split_into_chunks(
    raw_bytes: bytes, chunk_size: int, skip_empty: bool = True
) -> list[bytes]:
    """Split raw bytes into chunks of specified size."""
    if len(raw_bytes) % chunk_size != 0:
        raise ValueError(
            f"Raw bytes length {len(raw_bytes)} is not a multiple of chunk size {chunk_size}"
        )

    chunks = []

    for i in range(0, len(raw_bytes), chunk_size):
        chunk = raw_bytes[i : i + chunk_size]
        if skip_empty and chunk[0] == 0:
            continue
        chunks.append(chunk)

    return chunks


def int_from_slice(raw_bytes: bytes, byte_range: tuple) -> int:
    """Extract an integer from a slice of raw bytes."""
    return int.from_bytes(get_slice(raw_bytes, byte_range), "little")


def decode_gba_string(data: bytes) -> str:
    """Decode a GBA-encoded string from raw bytes, stopping at 0xFF."""
    chars = []
    for b in data:
        if b == 0xFF:
            break
        chars.append(CHARACTER_MAP.get(b, "?"))
    return "".join(chars)


def calculate_nature(personal_id: int) -> str:
    """
    Calculate the nature based on the personal ID.
    Args:
        personal_id (int): The personal ID of the Pokémon.
    Returns:
        str: The nature name.
    """
    return NATURES[personal_id % 25]


def unpack_ivs(ivs_data: int) -> list[int]:
    """
    Extracts the 6 IV values from a packed 32-bit integer.
    Returns: [iv_hp, iv_attack, iv_defense, iv_speed, iv_special_attack, iv_special_defense]
    """
    return [
        (ivs_data >> 0) & 0x1F,
        (ivs_data >> 5) & 0x1F,
        (ivs_data >> 10) & 0x1F,
        (ivs_data >> 20) & 0x1F,
        (ivs_data >> 25) & 0x1F,
        (ivs_data >> 15) & 0x1F,
    ]


def is_egg(ivs_data: int) -> bool:
    """Returns True if the Pokémon is an Egg, based on bit 30."""
    return bool((ivs_data >> 30) & 0x01)


def has_ha(ivs_data: int) -> bool:
    """Returns True if the Pokémon has a hidden ability, based on bit 31."""
    return bool((ivs_data >> 31) & 0x01)


def get_ability_index(pid: int) -> int:
    """
    Get the ability index based on the PID.
    1 = primary, 2 = secondary
    """
    return 1 if pid % 2 == 0 else 2


def unpack_moves(move_bytes: bytes) -> list[int]:
    """
    Extracts moves from a packed 5 byte value
    """
    val = int.from_bytes(move_bytes, "little")
    return [(val >> (10 * i)) & 0x3FF for i in range(4)]


def extract_moves(move_bytes: bytes) -> list[int]:
    """
    Extracts moves from an 8 byte field
    """
    return [int_from_slice(move_bytes, (i, i + 2)) for i in range(0, 8, 2)]


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
