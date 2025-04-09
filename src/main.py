from pokemon import read_pokemon_party, to_showdown_format, read_pokemon_boxes
from read_sav import read_sav_file
import paths

from io import BytesIO


def main():
    with open(paths.sav, "rb") as f:
        uploaded_file = BytesIO(f.read())

    sav_data = read_sav_file(uploaded_file, trim=True)
    party = read_pokemon_party(sav_data)
    boxes = read_pokemon_boxes(sav_data)

    export_text = ""
    for pokemon in party:
        export_text += to_showdown_format(pokemon) + "\n\n"

    for pokemon in boxes:
        export_text += to_showdown_format(pokemon) + "\n\n"

    print(export_text.strip())  # Print the formatted text to console


if __name__ == "__main__":
    main()
