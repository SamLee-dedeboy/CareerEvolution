import json
class DataManager():
    def __init__(self):
        self.artist_id_dict = loadJson("data/artist_name_dict.json")


def loadJson(filepath, map=lambda x: x):
    return map(json.load((open(filepath))))