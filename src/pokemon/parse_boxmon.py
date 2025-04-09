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
    unpack_moves,
    xp_to_lvl,
)


def parse_boxmon_entry(entry_data):
    """
    Parse the binary data for a single Pokémon entry in the box.
    """
    data_manager = GameDataManager()

    # Extract and assign values from the entry data

    personal_id = extract_poke_field(entry_data, "personal_id", type=1)
    species_id = extract_poke_field(entry_data, "species", type=1)
    species = data_manager.get_species_name(species_id)

    growth_rate = data_manager.get_growth_rate(species_id)
    xp = extract_poke_field(entry_data, "xp", type=1)
    level = xp_to_lvl(xp, growth_rate)

    held_item_id = extract_poke_field(entry_data, "held_item_id", type=1)
    held_item = data_manager.get_item_name(held_item_id)

    nickname_bytes = extract_raw_field(entry_data, "nickname")
    nickname = decode_gba_string(nickname_bytes) if nickname_bytes else ""

    evs = extract_multi_field(entry_data, "evs", 6, element_size=1, type=1)
    # Unpack EVs into individual variables
    ev_hp, ev_atk, ev_def, ev_spe, ev_spa, ev_spd = evs

    # Extract IVs and additional flags ; these are bit packed
    ivs_data = extract_poke_field(entry_data, "ivs_data", type=1)
    ivs = unpack_ivs(ivs_data)
    iv_hp, iv_atk, iv_def, iv_spe, iv_spa, iv_spd = ivs
    egg_status = is_egg(ivs_data)
    ha_status = has_hidden_ability(ivs_data)

    if personal_id % 2 == 0:
        ability_id = 1
    else:
        ability_id = 2

    ability = data_manager.get_ability_name(ability_id, species, ha_status)

    move_bytes = extract_raw_field(entry_data, "moves", type=1)
    move1, move2, move3, move4 = unpack_moves(move_bytes)

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
