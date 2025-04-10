from .parse_boxmon import parse_boxmon_entry
from .boxmon_extracter import extract_box_data, trim_boxmons

from read_sav import get_all_sections


def read_pokemon_boxes(sav_data):

    sections = get_all_sections(sav_data)
    boxmon_data = extract_box_data(sections)
    real_boxmons = trim_boxmons(boxmon_data)

    return [parse_boxmon_entry(boxmon) for boxmon in real_boxmons]
