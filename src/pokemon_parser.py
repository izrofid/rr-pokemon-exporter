from abc import ABC, abstractmethod
from pokemon import Pokemon, StatBlock
from data_manager import GameDataManager

from utils import (
    int_from_slice,
    get_slice,
    decode_gba_string,
    unpack_ivs,
    is_egg,
    has_ha,
    get_ability_index,
    extract_moves,
    unpack_moves,
    calculate_nature,
    xp_to_lvl,
)

from constants import POKEMON_SIZE, POKEMON_OFFSETS, BOXMON_OFFSETS, BOXMON_SIZE


class PokemonParser(ABC):
    @abstractmethod
    def parse(self, raw: bytes) -> Pokemon:
        """Parse a single Pokémon's raw bytes."""
        pass


class PartyPokemonParser(PokemonParser):
    def __init__(self):
        super().__init__()

    def parse(self, raw: bytes) -> Pokemon:
        """Parse a single Pokémon's raw bytes from the party."""

        if len(raw) != POKEMON_SIZE:
            raise ValueError(f"Invalid Pokémon data size: {len(raw)} bytes")

        # Values that need extra processing
        personal_id = int_from_slice(raw, POKEMON_OFFSETS["personal_id"])
        nickname_bytes = get_slice(raw, POKEMON_OFFSETS["nickname"])

        ivs_data = int_from_slice(raw, POKEMON_OFFSETS["ivs_data"])
        iv_list = unpack_ivs(ivs_data)

        ev_bytes = get_slice(raw, POKEMON_OFFSETS["evs"])
        ev_list = [ev_bytes[i] for i in (0, 1, 2, 4, 5, 3)]

        move_bytes = get_slice(raw, POKEMON_OFFSETS["moves"])

        # Actual values
        species_id = int_from_slice(raw, POKEMON_OFFSETS["species"])
        level = int_from_slice(raw, POKEMON_OFFSETS["level"])
        held_item_id = int_from_slice(raw, POKEMON_OFFSETS["held_item_id"])
        nickname = decode_gba_string(nickname_bytes)
        evs = StatBlock.from_list(ev_list)
        ivs = StatBlock.from_list(iv_list)
        is_egg_flag = is_egg(ivs_data)
        is_ha_flag = has_ha(ivs_data)
        ability_index = get_ability_index(personal_id)
        move_ids = extract_moves(move_bytes)
        nature = calculate_nature(personal_id)
        raw_data = raw
        sprite_url = f"https://raw.githubusercontent.com/izrofid/rrsprites/refs/heads/master/front/{species_id}.png"

        return Pokemon(
            species_id=species_id,
            level=level,
            held_item_id=held_item_id,
            nickname=nickname,
            evs=evs,
            ivs=ivs,
            is_egg_flag=is_egg_flag,
            has_ha_flag=is_ha_flag,
            ability_index=ability_index,
            move_ids=move_ids,
            nature=nature,
            raw_data=raw_data,
            sprite_url=sprite_url,
        )


class BoxPokemonParser(PokemonParser):
    def __init__(self):
        super().__init__()

    def parse(self, raw: bytes) -> Pokemon:
        """Parse a single Pokémon's raw bytes from the box."""
        if len(raw) != BOXMON_SIZE:
            raise ValueError(f"Invalid Pokémon data size: {len(raw)} bytes")

        # Data manager for growth rates
        gdm = GameDataManager()

        # Values that need extra processing
        personal_id = int_from_slice(raw, BOXMON_OFFSETS["personal_id"])
        species_id = int_from_slice(raw, BOXMON_OFFSETS["species"])

        xp = int_from_slice(raw, BOXMON_OFFSETS["xp"])
        growth_rate = gdm.get_growth_rate(species_id)

        nickname_bytes = get_slice(raw, BOXMON_OFFSETS["nickname"])

        ev_bytes = get_slice(raw, BOXMON_OFFSETS["evs"])
        ev_list = [ev_bytes[i] for i in (0, 1, 2, 4, 5, 3)]

        ivs_data = int_from_slice(raw, BOXMON_OFFSETS["ivs_data"])
        iv_list = unpack_ivs(ivs_data)

        move_bytes = get_slice(raw, BOXMON_OFFSETS["moves"])

        # Actual values
        # species_id = int_from_slice(raw, BOXMON_OFFSETS["species"])
        level = xp_to_lvl(xp, growth_rate)
        held_item_id = int_from_slice(raw, BOXMON_OFFSETS["held_item_id"])
        nickname = decode_gba_string(nickname_bytes)
        evs = StatBlock.from_list(ev_list)
        ivs = StatBlock.from_list(iv_list)
        is_egg_flag = is_egg(ivs_data)
        is_ha_flag = has_ha(ivs_data)
        ability_index = get_ability_index(personal_id)
        move_ids = unpack_moves(move_bytes)
        nature = calculate_nature(personal_id)
        raw_data = raw
        sprite_url = f"https://raw.githubusercontent.com/izrofid/rrsprites/refs/heads/master/front/{species_id}.png"

        return Pokemon(
            species_id=species_id,
            level=level,
            held_item_id=held_item_id,
            nickname=nickname,
            evs=evs,
            ivs=ivs,
            is_egg_flag=is_egg_flag,
            has_ha_flag=is_ha_flag,
            ability_index=ability_index,
            move_ids=move_ids,
            nature=nature,
            raw_data=raw_data,
            sprite_url=sprite_url,
        )
