from flask import Flask
from flask_cors import CORS
import json
from DataManager import DataManager

app = Flask(__name__)
CORS(app)

data_manager = DataManager()


@app.route("/data/artists")
def get_artists():
    return json.dumps(list(data_manager.artist_id_dict.values()), default=vars)