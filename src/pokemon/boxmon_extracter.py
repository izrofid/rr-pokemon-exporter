from constants import (
    SECTION_SIZE,
    VANILLA_BOX_SAVE_SECTIONS,
    VANILLA_MEMORY_BOX_COUNT,
    BOX_POKEMON_SIZE,
    MONS_PER_BOX,
    BOX_COUNT,
    BOX_MEMORY_START_OFFSET,
    CFRU_MON_SIZE,
)


def get_slice(data, start, length=None):
    """Extract a slice of bytes from the data."""
    if length is None:
        return data[start:]
    stop = start + length
    return data[start:stop]


def extract_box_pokemon_bytes(sections):
    """Extract raw Pokémon data bytes from the save blocks."""

    # Extract data from vanilla box memory (Boxes 1 - 19)
    raw_pokemon_data = get_slice(sections[5], 4)  # Skip the first four bytes

    for i in VANILLA_BOX_SAVE_SECTIONS[1:]:
        raw_pokemon_data += sections[i]

    raw_pokemon_data = raw_pokemon_data[
        : VANILLA_MEMORY_BOX_COUNT * MONS_PER_BOX * BOX_POKEMON_SIZE
    ]

    # Extract data from expanded box memory (Boxes 20 - 22)
    if BOX_COUNT >= 20:
        raw_pokemon_data += get_slice(
            sections[30], BOX_MEMORY_START_OFFSET[30], SECTION_SIZE
        )
        raw_pokemon_data += get_slice(sections[31], BOX_MEMORY_START_OFFSET[31], 0xF80)

    # Extract data from expanded box memory (Boxes 23 - 24)
    if BOX_COUNT >= 23:
        raw_pokemon_data += get_slice(
            sections[2], BOX_MEMORY_START_OFFSET[2], SECTION_SIZE
        )
        raw_pokemon_data += get_slice(sections[3], BOX_MEMORY_START_OFFSET[3], 0xCC0)

    # Extract data from expanded box memory (Box 25)
    if BOX_COUNT >= 25:
        raw_pokemon_data += get_slice(
            sections[0], BOX_MEMORY_START_OFFSET[0], BOX_POKEMON_SIZE * MONS_PER_BOX
        )

    return raw_pokemon_data


def trim_boxmons(raw_pokemon_data):
    """Trim the raw Pokémon data to filled slots."""

    trimmed_data = []
    for i in range(MONS_PER_BOX):

        start = i * CFRU_MON_SIZE
        stop = (i + 1) * CFRU_MON_SIZE
        entry_data = raw_pokemon_data[start:stop]

        if entry_data[0] == 0:
            continue  # Skip empty slots in boxes

        trimmed_data.append(entry_data)

    return trimmed_data
