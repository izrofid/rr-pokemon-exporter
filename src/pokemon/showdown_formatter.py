def to_showdown_format(pokemon_info):
    lines = []

    # Species and nickname
    species = pokemon_info["species"]
    nickname = pokemon_info["nickname"]

    held_item = pokemon_info.get("held_item_id", None)
    if held_item != "None":
        item_text = f" @ {held_item}"
    else:
        item_text = ""

    if nickname and nickname != species:
        lines.append(f"{nickname} ({species}){item_text}")
    else:
        lines.append(f"{species}{item_text}")

    # Level
    if pokemon_info.get("level") and pokemon_info["level"] != 100:
        lines.append(f"Level: {pokemon_info['level']}")

    # Nature
    if pokemon_info.get("nature"):
        lines.append(f"{pokemon_info['nature']} Nature")

    # Ability
    if pokemon_info.get("ability"):
        lines.append(f"Ability: {pokemon_info['ability']}")

    # Level
    if pokemon_info.get("level") and pokemon_info["level"] != 100:
        lines.append(f"Level: {pokemon_info['level']}")

    # Shiny, gender, happiness, etc. for later

    # EVs
    ev_parts = []
    ev_keys = [
        ("ev_hp", "HP"),
        ("ev_atk", "Atk"),
        ("ev_def", "Def"),
        ("ev_spa", "SpA"),
        ("ev_spd", "SpD"),
        ("ev_spe", "Spe"),
    ]
    for key, label in ev_keys:
        val = pokemon_info.get(key, 0)
        if val > 0:
            ev_parts.append(f"{val} {label}")
    if ev_parts:
        lines.append(f"EVs: {' / '.join(ev_parts)}")

    # IVs
    iv_parts = []
    iv_keys = [
        ("iv_hp", "HP"),
        ("iv_atk", "Atk"),
        ("iv_def", "Def"),
        ("iv_spa", "SpA"),
        ("iv_spd", "SpD"),
        ("iv_spe", "Spe"),
    ]
    for key, label in iv_keys:
        val = pokemon_info.get(key, 31)
        if val < 31:  # Only include if not perfect IV
            iv_parts.append(f"{val} {label}")
    if iv_parts:
        lines.append(f"IVs: {' / '.join(iv_parts)}")

    # Moves
    for i in range(1, 5):
        move = pokemon_info.get(f"move{i}")
        if move and move != "(No Move)":
            lines.append(f"- {move}")

    return "\n".join(lines)
