import streamlit as st
import tempfile
import os
from pokemon import read_pokemon_party, to_showdown_format, read_pokemon_boxes
from read_sav import read_sav_file
from markdowns import SIDEBAR, LINKS, WHERE_SAVE
from io import BytesIO


st.set_page_config(
    page_title="RR Pokémon Exporter",
    page_icon="https://raw.githubusercontent.com/JwowSquared/Radical-Red-Pokedex/master/favicon.ico",  # noqa: E501
    initial_sidebar_state="expanded",
)


SAVE_TYPES = ["sav", "sa1", "sa2", "sa3", "sa4"]


def main():
    st.title("Radical Red Pokémon Exporter")

    st.markdown(
        """
        **Upload your Radical Red save file to export your Pokémon in Showdown format.**
        """
    )

    col1, col2 = st.columns(2)
    with col1:
        # Streamlit radio button to choose between party and box Pokémon and both
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

    export_level = level_choice if set_level == "Yes" else 0

    uploaded_file = st.file_uploader(
        "Upload your save file", SAVE_TYPES, help=None, label_visibility="collapsed"
    )

    if not uploaded_file:
        with st.expander("Where is my save file?", expanded=False):
            st.markdown(WHERE_SAVE)

    if uploaded_file is not None:
        # Create a temporary file to save the uploaded content
        with tempfile.NamedTemporaryFile(delete=False, suffix=".sav") as tmp_file:
            # Write uploaded file content to the temp file
            tmp_file.write(uploaded_file.getvalue())
            tmp_path = tmp_file.name

        with open(tmp_path, "rb") as f:
            save_file = BytesIO(f.read())

        try:
            with st.spinner("Processing save file..."):
                sav_data = read_sav_file(save_file, trim=True)
                party = read_pokemon_party(sav_data)
                boxes = read_pokemon_boxes(sav_data)

                export_text = ""
                if export_choice in ("All", "Party"):
                    for pokemon in party:
                        export_text += (
                            to_showdown_format(pokemon, export_level) + "\n\n"
                        )

                if export_choice in ("All", "Box"):
                    for pokemon in boxes:
                        export_text += (
                            to_showdown_format(pokemon, export_level) + "\n\n"
                        )

                with st.expander(
                    f"📋{export_choice} Pokémon in Showdown Format",
                    expanded=True,
                ):
                    # Download button
                    st.download_button(
                        label="Download as Text File",
                        data=export_text.strip(),
                        file_name="pokemon_showdown_export.txt",
                        mime="text/plain",
                    )
                    # Display the text in a code block for easy copying
                    st.code(export_text.strip(), language="")

        except Exception as e:
            st.error(f"Error processing save file: {str(e)}")

        finally:
            # Clean up the temporary file
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

    with st.sidebar:
        st.header("RR Pokémon Exporter")
        st.markdown(SIDEBAR)
        st.markdown(LINKS)


if __name__ == "__main__":
    main()
