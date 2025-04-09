from .parse_pokemon import parse_pokemon_entry

from read_sav import (
    get_latest_block,
    get_frlg_sections,
)
from constants import (
    PARTY_OFFSET,
    POKEMON_SIZE,
    POKEMON_PARTY_SIZE,
)


def read_pokemon_party(sav_data):
    # latest_block = get_latest_block(sav_data)
    latest_block = get_latest_block(sav_data)
    sections = get_frlg_sections(latest_block)

    party_section = sections[1]

    # Extract party data
    party_data = party_section[
        PARTY_OFFSET : PARTY_OFFSET + POKEMON_SIZE * POKEMON_PARTY_SIZE
    ]

    party = []
    for i in range(POKEMON_PARTY_SIZE):
        entry_data = party_data[i * POKEMON_SIZE : (i + 1) * POKEMON_SIZE]
        if entry_data[0] == 0:
            break  # No more Pokémon in party
        pokemon = parse_pokemon_entry(entry_data)
        party.append(pokemon)

    return party
