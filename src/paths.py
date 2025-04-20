import os

DATA_DIR = "data"
SAV_DIR = "sav"
FONT_DIR = "fonts"


class BasePaths:
    def __init__(self):
        self.data = DataPaths()
        self.sav = SavPaths()
        self.fonts = FontPaths()


class DataPaths:
    def __init__(self):
        pass

    def __getattr__(self, name):
        return os.path.join(DATA_DIR, f"{name}.json")


class SavPaths:
    def __init__(self):
        pass

    def __getattr__(self, name):
        return os.path.join(SAV_DIR, f"{name}.sav")


class FontPaths:
    def __init__(self):
        pass

    def __getattr__(self, name):
        return os.path.join(FONT_DIR, f"{name}.ttf")


paths = BasePaths()
