from paths import BasePaths

from pokemon import Pokemon, StatBlock
from showdown_formatter import ShowdownFormatter
from data_manager import GameDataManager

from save_file import SaveFile
from pokemon_extractor import PartyPokemonExtractor, BoxPokemonExtractor
from pokemon_parser import PartyPokemonParser, BoxPokemonParser

paths = BasePaths()


def test_pokemon_to_showdown():
    evs = StatBlock.from_list([0, 0, 0, 252, 0, 252])
    ivs = StatBlock.from_list([31, 31, 31, 30, 31, 31])

    p = Pokemon(
        species_id=960,
        level=50,
        held_item_id=42,
        nickname="Bree",
        evs=evs,
        ivs=ivs,
        is_egg=False,
        has_hidden_ability=True,
        ability_index=1,
        move_ids=[43, 54, 56, 78],
        nature="Timid",
    )

    formatter = ShowdownFormatter(GameDataManager())

    print(formatter.format(p))


def test_party():
    with open(paths.sav.hijak, "rb") as f:
        raw = f.read()

    save = SaveFile(raw)

    party_extractor = PartyPokemonExtractor(save.active_block)
    party_parser = PartyPokemonParser()

    party = [party_parser.parse(p) for p in party_extractor.pokemon_in_party]

    formatter = ShowdownFormatter(GameDataManager())

    for mon in party:
        print(formatter.format(mon))


def test_box():
    with open(paths.sav.hijak, "rb") as f:
        raw = f.read()

    save = SaveFile(raw)

    box_extractor = BoxPokemonExtractor(save.active_block, save.expanded_block)

    box_parser = BoxPokemonParser()

    box = [box_parser.parse(p) for p in box_extractor.pokemon_in_storage]

    formatter = ShowdownFormatter(GameDataManager())

    for mon in box:
        print(formatter.format(mon))


if __name__ == "__main__":
    test_box()
