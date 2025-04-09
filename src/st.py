import streamlit as st
import tempfile
import os
from pokemon import read_pokemon_party, to_showdown_format, read_pokemon_boxes
from read_sav import read_sav_file
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
        Upload your Radical Red save file to export your Pokémon in Showdown format.

        This tool extracts all Pokémon from your PC boxes and converts them to a format
        that can be directly imported into Pokémon Showdown.
        """
    )

    uploaded_file = st.file_uploader(
        "Upload your save file", SAVE_TYPES, help="Select your Radical Red save file"
    )

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
                for pokemon in party:
                    export_text += to_showdown_format(pokemon) + "\n\n"

                for pokemon in boxes:
                    export_text += to_showdown_format(pokemon) + "\n\n"

                with st.expander(
                    "📋All Pokémon in Showdown Format",
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
        st.header("📋 Instructions")
        st.markdown(
            """
            1. **Upload** your Radical Red save file (`.sav`)
            2. **Wait** for processing to complete
            3. **Copy** the generated format or **download** as a text file
            4. **Import** into Pokémon Showdown
            """
        )

        st.header("ℹ️ About")
        st.markdown(
            """
            ### About This Tool
            This tool allows you to export Pokémon from **Radical Red** save files into
            **Pokémon Showdown** format.

            #### Features:
            - Extracts all Pokémon from your PC boxes.
            - Converts them into a format ready for **Pokémon Showdown**.
            - Provides an option to **download** the exported data as a text file.
            ---
            **Enjoy seamless Pokémon exporting!**
            """
        )


if __name__ == "__main__":
    main()
