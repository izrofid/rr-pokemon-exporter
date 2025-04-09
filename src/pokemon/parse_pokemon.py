from data_manager import GameDataManager

from utils import (
    decode_gba_string,
    extract_raw_field,
    extract_poke_field,
    extract_multi_field,
    calculate_nature,
    unpack_ivs,
    has_hidden_ability,
    is_egg,
)


def parse_pokemon_entry(entry_data):

    data_manager = GameDataManager()

    # Parse the binary data for a single Pokémon entry

    personal_id = extract_poke_field(entry_data, "personal_id")
    species_id = extract_poke_field(entry_data, "species")
    species = data_manager.get_species_name(species_id)

    level = extract_poke_field(entry_data, "level")

    held_item_id = extract_poke_field(entry_data, "held_item_id")
    held_item = data_manager.get_item_name(held_item_id)

    # Decode nickname using custom character encoding
    nickname_bytes = extract_raw_field(entry_data, "nickname")
    nickname = decode_gba_string(nickname_bytes) if nickname_bytes else ""

    evs = extract_multi_field(entry_data, "evs", 6, element_size=1)
    # Unpack EVs in to individual variables
    ev_hp, ev_atk, ev_def, ev_spe, ev_spa, ev_spd = evs

    # Extract IVs and additional flags ; these are bit packed
    ivs_data = extract_poke_field(entry_data, "ivs_data")
    ivs = unpack_ivs(ivs_data)
    iv_hp, iv_atk, iv_def, iv_spe, iv_spa, iv_spd = ivs
    egg_status = is_egg(ivs_data)
    ha_status = has_hidden_ability(ivs_data)

    if personal_id % 2 == 0:
        ability_id = 1
    else:
        ability_id = 2

    ability = data_manager.get_ability_name(ability_id, species, ha_status)

    moves = extract_multi_field(entry_data, "moves", 4, element_size=2)
    move1, move2, move3, move4 = moves
    move1 = data_manager.get_move_name(move1)
    move2 = data_manager.get_move_name(move2)
    move3 = data_manager.get_move_name(move3)
    move4 = data_manager.get_move_name(move4)

    nature = calculate_nature(personal_id)

    return {
        "species": species,
        "level": level,
        "held_item_id": held_item,
        "nickname": nickname,
        "ev_hp": ev_hp,
        "ev_atk": ev_atk,
        "ev_def": ev_def,
        "ev_spe": ev_spe,
        "ev_spa": ev_spa,
        "ev_spd": ev_spd,
        "iv_hp": iv_hp,
        "iv_atk": iv_atk,
        "iv_def": iv_def,
        "iv_spe": iv_spe,
        "iv_spa": iv_spa,
        "iv_spd": iv_spd,
        "is_egg": egg_status,
        "ability": ability,
        "move1": move1,
        "move2": move2,
        "move3": move3,
        "move4": move4,
        "nature": nature,
    }
