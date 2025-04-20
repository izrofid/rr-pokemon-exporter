import os

DATA_DIR = "data"
SAV_DIR = "sav"


class BasePaths:
    def __init__(self):
        self.data = DataPaths()
        self.sav = SavPaths()


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


paths = BasePaths()
