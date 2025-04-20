from dataclasses import dataclass


@dataclass
class StatBlock:
    hp: int
    attack: int
    defense: int
    special_attack: int
    special_defense: int
    speed: int

    @classmethod
    def from_list(cls, stats: list[int]) -> "StatBlock":
        """Create a StatBlock from a list of stats."""
        return cls(*stats)

    def to_dict(self) -> dict:
        """Convert the stats to a dictionary."""
        return {
            "HP": self.hp,
            "Atk": self.attack,
            "Def": self.defense,
            "SpA": self.special_attack,
            "SpD": self.special_defense,
            "Spe": self.speed,
        }

    def __getitem__(self, key: str) -> int:
        return self.to_dict()[key]


@dataclass
class Pokemon:
    """Holds all the information about a Pokémon."""

    species_id: int
    level: int
    held_item_id: int | None
    nickname: str | None
    evs: StatBlock
    ivs: StatBlock
    is_egg_flag: bool
    has_ha_flag: bool
    ability_index: int
    move_ids: list[int]
    nature: str
    raw_data: bytes = b""
