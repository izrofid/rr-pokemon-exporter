from data_manager import GameDataManager
from pokemon import Pokemon
import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from collections import Counter
import numpy as np
from paths import BasePaths

paths = BasePaths()


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

    def format_image(self, party: list[Pokemon]) -> Image.Image:
        sprite_size = (96, 96)
        spacing_x = 20
        spacing_y = 10
        padding_x = 20
        padding_y = 20
        col_count = 2
        row_count = (len(party) + 1) // 2

        box_width = 400
        image_width = col_count * box_width + spacing_x * (col_count - 1)

        row_height = sprite_size[1] + 100
        content_height = (row_count * row_height) + (spacing_y * (row_count - 1))
        image_height = content_height + (padding_y)

        canvas = Image.new("RGBA", (image_width, image_height), (18, 18, 18, 255))
        draw = ImageDraw.Draw(canvas)

        try:
            font = ImageFont.truetype(paths.fonts.pixeloperator, 16)

        except Exception as e:  # noqa
            print(e)

        for idx, p in enumerate(party):
            col = idx % col_count
            row = idx // col_count
            x = col * (box_width + spacing_x)

            # Only add spacing_y for rows that aren't the last row
            x = padding_x + col * (box_width + spacing_x)
            y = padding_y + (row * row_height) + (spacing_y * row)

            try:
                if p.sprite_url.startswith("http"):
                    response = requests.get(p.sprite_url)
                    sprite = Image.open(BytesIO(response.content)).convert("RGBA")
                else:
                    sprite = Image.open(p.sprite_url).convert("RGBA")

                # Get border pixels to determine background color
                width, height = sprite.size
                border_pixels = []
                for border_y in range(height):
                    border_pixels.append(sprite.getpixel((0, border_y)))
                    border_pixels.append(sprite.getpixel((width - 1, border_y)))
                for border_x in range(width):
                    border_pixels.append(sprite.getpixel((border_x, 0)))
                    border_pixels.append(sprite.getpixel((border_x, height - 1)))

                # Find most common border color
                bg_color = Counter(border_pixels).most_common(1)[0][0]

                # Make matching pixels transparent
                data = sprite.getdata()
                new_data = []
                for item in data:

                    if item[:3] == bg_color[:3]:
                        new_data.append((0, 0, 0, 0))
                    else:
                        new_data.append(item)
                sprite.putdata(new_data)

            except Exception as e:
                print(f"Could not load sprite for species ID {p.species_id}: {e}")
                continue

            sprite = sprite.resize(sprite_size)
            canvas.paste(sprite, (x, y), sprite)

            sprite_array = np.array(sprite)

            mask = sprite_array[..., 3] > 0

            if mask.any():

                avg_color = np.mean(sprite_array[mask][:, :3], axis=0)

                brightness = (
                    avg_color[0] * 299 + avg_color[1] * 587 + avg_color[2] * 114
                ) / 1000
                bg_brightness = (18 * 299 + 18 * 587 + 18 * 114) / 1000

                min_contrast = 148
                if abs(brightness - bg_brightness) < min_contrast:
                    adjustment = 1.5
                    avg_color = np.minimum(255, avg_color * adjustment)

                dominant_color = tuple(map(int, avg_color))
            else:
                dominant_color = (255, 255, 255)

            # Showdown text
            text_x = x + sprite_size[0] + 10
            text_y = y
            showdown_text = self.format(p).strip().split("\n")

            # Color definitions
            text_color = (255, 255, 255)  # White for main text
            label_color = (170, 170, 170)  # Light grey for labels
            stat_colors = {
                "HP": (255, 0, 0),  # Red
                "Atk": (240, 128, 48),  # Orange
                "Def": (248, 208, 48),  # Yellow
                "SpA": (104, 144, 240),  # Blue
                "SpD": (120, 200, 80),  # Green
                "Spe": (248, 88, 136),  # Pink
            }

            # Draw each line with appropriate color
            for i, line in enumerate(showdown_text):
                if i == 0:  # First line is Pokemon name/species
                    draw.text(
                        (text_x, text_y),
                        line,
                        font=font,
                        fill=dominant_color,
                        stroke_width=0,
                        stroke_fill=None,
                    )
                elif line.startswith("EVs:"):
                    current_x = text_x
                    # Draw the "EVs:" label in grey
                    draw.text((current_x, text_y), "EVs:", font=font, fill=label_color)
                    current_x += font.getlength("EVs: ")

                    # Split the EV values
                    ev_parts = line[4:].strip().split(" / ")

                    for i, ev_part in enumerate(ev_parts):
                        # For each stat (e.g., "252 HP")
                        value, stat = ev_part.strip().split(" ")

                        # Draw the value and stat in the stat's color
                        stat_text = f"{value} {stat}"
                        draw.text(
                            (current_x, text_y),
                            stat_text,
                            font=font,
                            fill=stat_colors[stat],
                        )
                        current_x += font.getlength(stat_text)

                        # Draw slash in white if not the last stat
                        if i < len(ev_parts) - 1:
                            draw.text(
                                (current_x, text_y), " / ", font=font, fill=text_color
                            )
                            current_x += font.getlength(" / ")

                elif line.startswith("IVs:"):
                    current_x = text_x
                    # Draw the "IVs:" label in grey
                    draw.text((current_x, text_y), "IVs:", font=font, fill=label_color)
                    current_x += font.getlength("IVs: ")

                    # Split the IV values
                    iv_parts = line[4:].strip().split(" / ")

                    for i, iv_part in enumerate(iv_parts):
                        # For each stat (e.g., "0 Atk")
                        value, stat = iv_part.strip().split(" ")

                        # Draw the value and stat in the stat's color
                        stat_text = f"{value} {stat}"
                        draw.text(
                            (current_x, text_y),
                            stat_text,
                            font=font,
                            fill=stat_colors[stat],
                        )
                        current_x += font.getlength(stat_text)

                        # Draw slash in white if not the last stat
                        if i < len(iv_parts) - 1:
                            draw.text(
                                (current_x, text_y), " / ", font=font, fill=text_color
                            )
                            current_x += font.getlength(" / ")
                elif any(label in line for label in ["Level:", "Nature", "Ability:"]):
                    # Split the line at the colon if present
                    if ":" in line:
                        label, value = line.split(":", 1)
                        draw.text(
                            (text_x, text_y), f"{label}:", font=font, fill=label_color
                        )
                        draw.text(
                            (text_x + font.getlength(f"{label}:"), text_y),
                            value,
                            font=font,
                            fill=text_color,
                        )
                    else:
                        draw.text((text_x, text_y), line, font=font, fill=label_color)
                else:
                    draw.text(
                        (text_x, text_y),
                        line,
                        font=font,
                        fill=text_color,
                        stroke_width=0,
                        stroke_fill=None,
                    )

                text_y += font.getbbox(line)[3] + 2

        return canvas

    def get_image_bytes(self, party: list[Pokemon]) -> BytesIO:
        img = self.format_image(party)
        buf = BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)
        return buf
