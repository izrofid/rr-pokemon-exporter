# noqa E501
SIDEBAR = """
## About This Tool

Easily export your Pokémon from Radical Red save files into a format you can use on **Pokémon Showdown**! (And all Radic
al Red tools that use the format)

**What it does:**
- Grabs all Pokémon from your Party and PC boxes
- Converts them into Showdown-ready format
- Lets you download everything as a `.txt` file
- **Grabs IV and EV data**
- Works with mGBA Flash 128k + RTC save files

No longer shall you have to manually enter stuff into the calc!!
            """

LINKS = """
## Links
[Radical Red Showdown Server](https://play.radicalred.net)

[Radical Red Official Calculator](https://calc.radicalred.net/)

[Radical Red Normal Mode Calculator by Hzla](https://hzla.github.io/Dynamic-Calc-Decomps/?data=ced457ba9aa55731616c&dmgGen=8&gen=8&types=6&noSwitch=1)

[RR Pokemon Locations by me](https://rrlocations.streamlit.app/)

[This Project](https://github.com/izrofid/rr-pokemon-exporter)


## Credits
Huge thanks to [Bulbapedia](https://bulbapedia.bulbagarden.net/wiki/Save_data_structure_%28Generation_III%29) for explaining the vanilla save structure and [eliyahu1702](https://github.com/eliyahu1702/Rad-Red-4.1-Team-Exporter) and [skeli789](https://github.com/Skeli789/Unbound-Cloud) for referencing CFRU structure.
"""

WHERE_SAVE = """
###  Where is my save file?

**🕹️ mGBA (PC):**

> Saves are usually stored in the same folder as the ROM, with a `.sav`,
> `.sa2`, `.sa3`, etc. extension depending on the save slot used.



```
RadicalRed.sav
RadicalRed.sa2
RadicalRed.sa3
```

**🕹️ VBA-M (VisualBoyAdvance-M):**

> Save files are typically `.sav` and stored next to the ROM.

```
RadicalRed.sav
```

**📱 Delta (iOS):**

> Saves are accessible through the **Files** app.

```
On My iPhone > Delta > Saves
```

**📱 Android Emulators (e.g., MyBoy!, Pizza Boy):**

> Save files are stored in app folders on internal storage.

```
Internal Storage > MyBoy > save
```

**💡 Tip:**
Emulators that use the **128K Flash + RTC** save format are fully supported.
You can drop in `.sav`, `sa2`, `sa3`, `sa4`, etc. directly — *no conversion needed*.
"""
