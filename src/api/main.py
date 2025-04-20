from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from save_file import SaveFile
from pokemon_extractor import PartyPokemonExtractor, BoxPokemonExtractor
from pokemon_parser import PartyPokemonParser, BoxPokemonParser
from showdown_formatter import ShowdownFormatter
from data_manager import GameDataManager

# Create the FastAPI app
app = FastAPI(title="RR Pokemon Exporter")

# Allow requests from our frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Your Vite dev server address
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/upload")
async def upload_save(save_file: UploadFile):
    """Handle save file upload and return parsed Pokémon data"""
    if not any(save_file.filename.endswith(ext) for ext in [".sav", ".sa2", ".sa3", ".sa4"]):
        raise HTTPException(
            status_code=400, detail="Invalid file type. Please upload a .sav file"
        )

    try:
        # Read the uploaded file
        contents = await save_file.read()

        # Create SaveFile instance
        save = SaveFile(contents)

        # Extract party Pokémon
        party_extractor = PartyPokemonExtractor(save.active_block)
        party_parser = PartyPokemonParser()
        party_pokemon = [
            party_parser.parse(pokemon) for pokemon in party_extractor.pokemon_in_party
        ]

        # Extract box Pokémon
        box_extractor = BoxPokemonExtractor(save.active_block, save.expanded_block)
        box_parser = BoxPokemonParser()
        box_pokemon = [
            box_parser.parse(pokemon) for pokemon in box_extractor.pokemon_in_storage
        ]

        # Format everything for Showdown
        formatter = ShowdownFormatter(GameDataManager())

        return {
            "party": [formatter.format(mon) for mon in party_pokemon],
            "box": [formatter.format(mon) for mon in box_pokemon],
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
