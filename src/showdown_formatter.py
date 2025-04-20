from data_manager import GameDataManager
from pokemon import Pokemon


class ShowdownFormatter:
    def __init__(self, data: GameDataManager, export_level: int | None = None):
        self.data = data
        self.export_level = export_level

    def format(self, p: Pokemon) -> str:
        species = self.data.get_species_name(p.species_id)
        held_item = self.data.get_item_name(p.held_item_id)
        moves = [self.data.get_move_name(m) for m in p.move_ids]
        ability = self.data.get_ability_name(p.ability_index, species, p.has_ha_flag)

        level = p.level if self.export_level is None else self.export_level

        name_line = (
            f"{p.nickname} ({species})"
            if p.nickname and p.nickname != species
            else species
        )
        item_line = f" @ {held_item}" if held_item != "None" else ""

        evs_str = " / ".join(f"{v} {k}" for k, v in p.evs.to_dict().items() if v > 0)
        ivs_str = " / ".join(f"{v} {k}" for k, v in p.ivs.to_dict().items() if v != 31)

        lines = [
            f"{name_line}{item_line}",
            f"Level: {level}",
            f"{p.nature} Nature",
            f"Ability: {ability or 'Unknown'}",
        ]
        if ivs_str:
            lines.append(f"IVs: {ivs_str}")
        if evs_str:
            lines.append(f"EVs: {evs_str}")
        lines.extend(f"- {m}" for m in moves if m)

        return "\n".join(lines) + "\n"
