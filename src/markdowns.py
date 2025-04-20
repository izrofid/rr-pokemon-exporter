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

FAQ = """

### FAQ

#### What is this tool?

This tool reads your Radical Red v4.1 save file and exports your party Pokémon in a format you can copy-paste into Pokémon Showdown’s Team Builder or the Radical Red calculators.

---

#### What kind of file should I upload?
You should upload your **in-game save file**, which ends in `.sav` or `.saveRAM`. This is created when you save the game using the **Start > Save** option from the main menu inside the game. mGBA's player specific save extensions (`.sa2` for player 2 saves) are fine
---

#### Can I use a save state?
**No.** Save states (like `.sgm`, `.state`,  etc.) are not supported. These are emulator-specific and do not contain your actual game data in a usable format.
Always use your proper `.sav` file created through in-game saving.

---

#### What version of Radical Red is this for?
This tool is designed specifically for **Radical Red v4.1**. It may not work correctly with earlier versions due to changes in how save data is stored.

---

#### Why does it throw an error?
- You might’ve uploaded the wrong file (like a save state).
- You may not have any Pokémon in your party yet.
---



#### Is this safe to use?
Yes. Your save file is not edited in anyway. This simply reads the `.sav` and extracts information from it.

---

#### How do I use the exported data?
Once your Pokémon are listed, just copy the text and paste it directly into a calculator or the Showdown Teambuilder. It will include details like nickname, nature, ability, level, and moves.

---

#### I'm on iOS and I can't upload my save file. Why?
This is a known issue. Unfortunately I don't use an iOS device so it's difficult to figure out what's wrong. You can copy the file to another device and upload it from there. This will be fixed as soon as I can figure it out.

"""
