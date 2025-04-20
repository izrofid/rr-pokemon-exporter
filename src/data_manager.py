import json
from pathlib import Path


class GameDataManager:
    """Singleton manager for all game data resources (species, moves, abilities, etc.)"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GameDataManager, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self) -> None:
        """Initialize all data resources"""
        self.species_data = SpeciesDataProvider()
        self.move_data = MoveDataProvider()
        self.ability_data = AbilityDataProvider()
        self.item_data = ItemDataProvider()
        self.growth_rate_data = GrowthRateProvider()

    def get_species_name(self, species_id: int) -> str:
        """Get a Pokémon's name by its species ID"""
        return self.species_data.get_name(species_id)

    def get_move_name(self, move_id: int) -> str:
        """Get a move name by its ID"""
        return self.move_data.get_name(move_id)

    def get_ability_name(
        self, ability_id: int, pokemon_name: str, has_hidden_ability: bool
    ) -> str:
        """Get an ability name by its index (1, 2, or 3 for hidden) and Pokemon name"""
        return self.ability_data.get_ability_name(
            ability_id, pokemon_name, has_hidden_ability
        )

    def get_growth_rate(self, species_id: int) -> str:
        """Get the growth rate for a Pokémon by its species ID"""
        return self.growth_rate_data.get_growth_rate(species_id)

    def get_item_name(self, item_id: int) -> str:
        """Get an item name by its ID"""
        return self.item_data.get_name(item_id)


class DataProvider:
    """Base class for all data providers"""

    def __init__(self, filename: str) -> None:
        self.data_path = Path(__file__).parent.parent / "data" / filename
        self._data = self._load_data()

    def _load_data(self) -> object:
        """Load data from JSON file"""
        try:
            with open(self.data_path, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading data from {self.data_path.name}: {e}")
            return {}


class SpeciesDataProvider(DataProvider):
    """Provider for Pokémon species data"""

    def __init__(self) -> None:
        super().__init__("species.json")

    def get_name(self, species_id: int) -> str:
        """Get a Pokémon's name by its species ID"""
        if isinstance(self._data, list) and 1 <= species_id <= len(self._data):
            return self._data[species_id - 1]
        return f"Unknown ({species_id})"


class MoveDataProvider(DataProvider):
    """Provider for Pokémon move data"""

    def __init__(self) -> None:
        super().__init__("moves.json")

    def get_name(self, move_id: int) -> str | None:
        """Get a move name by its ID"""
        if isinstance(self._data, list) and 1 <= move_id <= len(self._data):
            return self._data[move_id - 1]
        elif move_id == 0:
            return None
        else:
            return f"Unknown ({move_id})"


class AbilityDataProvider(DataProvider):
    """Provider for Pokémon ability data"""

    def __init__(self) -> None:
        super().__init__("abilities.json")

    def get_ability_name(
        self, ability_id: int, pokemon_name: str, has_hidden_ability: bool
    ) -> str:
        """
        Get ability name by index and Pokemon name
        ability_index: 1 = primary, 2 = secondary, 3 = hidden
        """
        if pokemon_name not in self._data:
            return f"Unknown Ability (for {pokemon_name})"

        ha = self._data[pokemon_name].get("hidden_ability")

        if has_hidden_ability and ha is not None:
            return self._data[pokemon_name].get("hidden_ability")

        elif ability_id == 1:
            return self._data[pokemon_name].get("primary_ability")

        elif ability_id == 2:
            return self._data[pokemon_name].get("secondary_ability")
        else:
            return f"Found Nothing (for {pokemon_name} ability_id: {ability_id} ha: {has_hidden_ability})"


class GrowthRateProvider(DataProvider):
    """Provider for Pokémon growth rate data"""

    def __init__(self) -> None:
        super().__init__("growth_rates.json")

    def get_growth_rate(self, species_id: int) -> str:
        """Get the growth rate for a Pokémon by its species ID"""
        if isinstance(self._data, list) and 0 <= species_id < len(self._data):
            growth_rate = self._data[species_id - 1].get("growth_rate")
            if growth_rate:
                return growth_rate
        return "medium"  # Default to medium if not found


class ItemDataProvider(DataProvider):
    """Provider for Pokémon item data"""

    def __init__(self) -> None:
        super().__init__("items.json")

    def get_name(self, item_id: int) -> str:
        """Get an item name by its ID"""
        if item_id == 0:
            return "None"
        if isinstance(self._data, list) and 1 <= item_id <= len(self._data):
            return self._data[item_id - 1]
        return f"Unknown Item ({item_id})"
