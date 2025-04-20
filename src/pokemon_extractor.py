from save_block import SaveBlock
from utils import get_slice, split_into_chunks
from loggers import logger

from constants import (
    PARTY_OFFSET,
    POKEMON_SIZE,
    BOX_OFFSETS,
    FRLG_BOX_SECTIONS,
    CFRU_BOX_SECTIONS,
    BOXMON_SIZE,
)


class PartyPokemonExtractor:
    def __init__(self, active_block: SaveBlock):
        self.active_block = active_block

    @property
    def pokemon_in_party(self) -> list[bytes]:
        """Extract party Pokémon data from the active block."""
        party_pokemon = []

        party_section = self.active_block.get_section(1)

        party_data = get_slice(party_section.data, PARTY_OFFSET)

        party_pokemon = split_into_chunks(party_data, POKEMON_SIZE, skip_empty=True)

        return party_pokemon


class BoxPokemonExtractor:
    def __init__(self, active_block: SaveBlock, expanded_block: SaveBlock):
        """Extract box Pokémon data from the active block."""
        self.active_block = active_block
        self.expanded_block = expanded_block

    @property
    def pokemon_in_storage(self) -> list[bytes]:
        """Extract box Pokémon data from the active block."""
        box_pokemon = []

        # Extract vanilla boxes
        res = []
        for sid in FRLG_BOX_SECTIONS:
            section = self.active_block.get_section(sid)
            box_bytes = get_slice(section.data, BOX_OFFSETS[sid])
            res.append(box_bytes)
            logger.debug(f"box bytes has length of {len(box_bytes)}")

        # Extract CFRU boxes
        for sid in CFRU_BOX_SECTIONS:
            if sid not in [30, 31]:
                section = self.active_block.get_section(sid)
            else:
                section = self.expanded_block.get_section(sid)
            box_bytes = get_slice(section.data, BOX_OFFSETS[sid])
            res.append(box_bytes)

        # Combine all boxes into raw bytes
        box_data = b"".join(res)

        box_pokemon = split_into_chunks(box_data, BOXMON_SIZE, skip_empty=True)

        return box_pokemon
