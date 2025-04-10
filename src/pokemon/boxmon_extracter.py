from typing import Optional
from constants import (
    VANILLA_BOX_SAVE_SECTIONS,
    VANILLA_MEMORY_BOX_COUNT,
    MONS_PER_BOX,
    BOX_COUNT,
    BOX_MEMORY_START_OFFSET,
    CFRU_MON_SIZE,
    SEC_DATA_SIZE
)


def get_slice(data: list, start: int, length: Optional[int] = None) -> list:
    """Extract a slice of bytes from the data."""
    if length is None:
        return data[start:]
    stop = start + length
    return data[start:stop]


def extract_box_data(sections: dict[int, list[int]]) -> list[int]:
    """
    Reconstructs and returns a flat list of all box Pokémon data across
    boxes 1-25 in a CFRU save file. Each Pokémon is 58 bytes (CFRU compressed).

    The function handles both the vanilla and expanded box memory layouts.
    Total expected size: 750 Pokémon x 58 bytes = 43,500 bytes.

    :param sections: Dictionary of save sections by ID (0-1), each a list of 4096 bytes
    :return: A flat list of bytes containing all 750 Pokémon (25 boxes)
    """

    # ------------------------
    # Boxes 1–19 (Vanilla layout, Sections 5–13)
    # ------------------------

    # Start with section 5 (skip first 4 bytes: current box index stored there)
    result = sections[5][4:]

    # Add entire contents of sections 6–13 (each holds one full box)
    for sid in VANILLA_BOX_SAVE_SECTIONS[1:]:
        result += sections[sid]

    # Cut off any extra bytes beyond the expected 19 boxes × 1740 bytes
    result = result[: VANILLA_MEMORY_BOX_COUNT * MONS_PER_BOX * CFRU_MON_SIZE]
    # 19 × 30 × 58 = 33,060 bytes

    # ------------------------
    # Boxes 20–22 (Section 30 + 31, starts at offset 0xB0C)
    # ------------------------

    if BOX_COUNT >= 20:
        # Start at 0xB0C in section 30 and read until the end (4080 = 0xFF0)
        result += sections[30][BOX_MEMORY_START_OFFSET[30] : SEC_DATA_SIZE]
        # Then continue from section 31 up to offset 0xF80 (remaining 3968 bytes)
        result += sections[31][BOX_MEMORY_START_OFFSET[31] : 0xF80]
        # This gives us 3 boxes × 1740 = 5220 bytes

    # ------------------------
    # Boxes 23–24 (Section 2 + 3, starts at 0xF18 in section 2)
    # ------------------------

    if BOX_COUNT >= 23:
        # Read from 0xF18 to end of section 2 (3968)
        result += sections[2][BOX_MEMORY_START_OFFSET[2] : SEC_DATA_SIZE]
        # Then continue from start of section 3 up to 0xCC0
        result += sections[3][BOX_MEMORY_START_OFFSET[3] : 0xCC0]
        # This gives us 2 boxes × 1740 = 3480 bytes

    # ------------------------
    # Box 25 (From section 0, starting at 0xB0)
    # ------------------------

    if BOX_COUNT >= 25:
        start = BOX_MEMORY_START_OFFSET[0]
        size = CFRU_MON_SIZE * MONS_PER_BOX  # 58 × 30 = 1740
        result += sections[0][start : start + size]

    # ------------------------
    # Final flat byte list
    # ------------------------

    return result


def trim_boxmons(raw_pokemon_data):
    """Trim the raw Pokémon data to filled slots."""

    trimmed_data = []
    for i in range(MONS_PER_BOX * BOX_COUNT):

        start = i * CFRU_MON_SIZE
        stop = (i + 1) * CFRU_MON_SIZE
        entry_data = raw_pokemon_data[start:stop]

        if entry_data[0] == 0:
            continue  # Skip empty slots in boxes

        trimmed_data.append(entry_data)

    return trimmed_data
