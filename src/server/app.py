from flask import Flask
from flask_cors import CORS
import json
from DataManager import DataManager

app = Flask(__name__)
CORS(app)

data_manager = DataManager()


@app.route("/data/artists")
def get_artists():
    return json.dumps(data_manager.artist_infos, default=vars)

@app.route("/data/career/<artist_id>")
def get_career(artist_id):
    return json.dumps(data_manager.loadCareer(artist_id))

@app.route("/data/info/<artist_id>")
def get_info(artist_id):
    return json.dumps(data_manager.loadInfo(artist_id))