import streamlit as st
import tempfile
import os

from showdown_formatter import ShowdownFormatter
from data_manager import GameDataManager

from save_file import SaveFile
from pokemon_extractor import PartyPokemonExtractor, BoxPokemonExtractor
from pokemon_parser import PartyPokemonParser, BoxPokemonParser

from markdowns import SIDEBAR, WHERE_SAVE, LINKS, FAQ


st.set_page_config(
    page_title="RR Pokémon Exporter",
    page_icon="https://raw.githubusercontent.com/JwowSquared/Radical-Red-Pokedex/master/favicon.ico",  # noqa: E501
    initial_sidebar_state="expanded",
)

SAVE_TYPES = ["sav", "sa1", "sa2", "sa3", "sa4", "saveram", "srm", "bin"]


def main():
    st.title("Radical Red Pokémon Exporter")

    st.markdown(
        """
        **Upload your Radical Red save file to export your Pokémon in Showdown format.**
        """
    )

    (
        col1,
        col2,
    ) = st.columns(2)
    with col1:

        export_choice = st.radio(
            "Select Pokémon to export",
            ("All", "Party", "Box"),
            index=0,
            horizontal=True,
        )

    with col2:
        set_level = st.radio(
            "Select level to export?",
            ("Yes", "No"),
            index=1,
            horizontal=True,
        )

    level_choice = st.number_input(
        "Export Level", min_value=1, max_value=100, value=50, disabled=set_level == "No"
    )

    export_level = level_choice if set_level == "Yes" else None

    uploaded_file = st.file_uploader(
        "Upload your save file", SAVE_TYPES, help=None, label_visibility="collapsed"
    )

    with st.expander("FAQ", expanded=False):
        st.markdown(FAQ)

    if not uploaded_file:
        with st.expander("Where is my save file?", expanded=False):
            st.markdown(WHERE_SAVE)

    if uploaded_file is not None:

        with tempfile.NamedTemporaryFile(delete=False, suffix=".sav") as tmp_file:

            tmp_file.write(uploaded_file.getvalue())
            tmp_path = tmp_file.name

        with open(tmp_path, "rb") as f:
            raw = f.read()

        try:
            with st.spinner("Processing save file..."):
                save = SaveFile(raw)
                export_text = ""

                party_extractor = PartyPokemonExtractor(save.active_block)
                party_parser = PartyPokemonParser()

                box_extractor = BoxPokemonExtractor(
                    save.active_block, save.expanded_block
                )
                box_parser = BoxPokemonParser()

                box = [box_parser.parse(p) for p in box_extractor.pokemon_in_storage]

                party = [
                    party_parser.parse(p) for p in party_extractor.pokemon_in_party
                ]

                formatter = ShowdownFormatter(GameDataManager(), export_level)

                party_mons = [formatter.format(mon) for mon in party]
                box_mons = [formatter.format(mon) for mon in box]

                image_bytes = formatter.get_image_bytes(party)

                if export_choice == "All" or export_choice == "Party":
                    export_text += "\n".join(party_mons) + "\n\n"
                if export_choice == "All" or export_choice == "Box":
                    export_text += "\n".join(box_mons) + "\n\n"

                with st.expander(
                    f"{export_choice} Pokémon in Showdown Format",
                    expanded=True,
                ):

                    if export_choice != "Box":
                        tab1, tab2 = st.tabs(["Text", "Image"])
                        with tab1:
                            st.download_button(
                                label="Download as Text File",
                                data=export_text.strip(),
                                file_name="pokemon_showdown_export.txt",
                                mime="text/plain",
                            )
                            st.code(export_text.strip(), language="")

                        with tab2:
                            st.download_button(
                                label="Download Image",
                                data=image_bytes,
                                file_name="pokemon_team_image.png",
                                mime="image/png",
                            )
                            st.image(
                                image_bytes,
                                caption="Your Team",
                                use_container_width=True,
                            )

                    else:
                        st.download_button(
                            label="Download as Text File",
                            data=export_text.strip(),
                            file_name="pokemon_showdown_export.txt",
                            mime="text/plain",
                        )
                        st.code(export_text.strip(), language="")

        except Exception as e:
            st.exception(e)

        finally:

            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

    with st.sidebar:
        st.header("RR Pokémon Exporter")
        st.markdown(SIDEBAR)
        st.markdown(LINKS)


if __name__ == "__main__":
    main()
