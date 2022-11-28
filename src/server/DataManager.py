import json
from collections import defaultdict
from pprint import pprint
import re
class DataManager():
    def __init__(self):
        self.artist_infos = loadJson(r"data/target_actor_info.json")
        self.movie_infos = loadJson(r"data/movie_pool.json")
        self.careers = loadJson(r"data/career_w_snippets.json")
        self.snippets_path = "data/career_snippets/"

    def loadCareer(self, artist_id):
        career = self.careers[artist_id]
        return self.preprocess_career(artist_id, self.add_infos(career))

    def add_infos(self, career):
        if not career: return [] 
        movie_infos = []
        for movie in career:
            movie_id = movie['tid']
            role = movie['role']
            movie_snippet = movie['wiki_description']
            movie_info = self.get_movie_info(movie_id)
            movie_infos.append({
                "id": movie_id,
                "title": movie_info['title'],
                "votes": movie_info['votes'],
                "rating": movie_info['ratings'],
                "genre": movie_info['genre'],
                "year": movie_info['year'],
                "role": role,
                "snippet": movie_snippet,
            })
        return movie_infos
    
    def preprocess_career(self, artist_id, movie_infos):
        movie_infos.sort(key=lambda movie: int(movie['year']))
        stages = {}
        empty_movies = []
        cur_stage = ""
        for movie_info in movie_infos:
            if not movie_info['snippet']: 
                empty_movies.append(movie_info)
                continue
            # create a stage 
            header = decideHeader(movie_info['snippet'])
            movie_info['snippet'] = filter_snippets(header, movie_info['snippet'])
            if header != cur_stage:
                new_stage = {
                    "header": header,
                    "paragraphs": set(),
                    "movies": empty_movies
                }
                stages[header] = new_stage
                cur_stage = header
            else:
                stages[cur_stage]['movies'] += empty_movies
            stages[header]['movies'].append(movie_info)
            empty_movies = []
            for sentence in movie_info['snippet']:
                paragraph = sentence['p']
                new_stage['paragraphs'].add(paragraph)

        if empty_movies:
            stages[cur_stage]["movies"] += empty_movies

        # post process
        stages_list = []
        for header, stage in stages.items():
            stage['paragraphs'] = list(stage['paragraphs'])
            stages_list.append({
                "header": header,
                "paragraphs": self.getParagraphs(artist_id, header, stage['paragraphs']),
                "movies": stage['movies']
            })
        return stages_list
        
    def getParagraphs(self, actor_id, target_header, target_pids):
        snippets = json.load(open(self.snippets_path + actor_id + ".json"))['career']
        paragraphs = []
        for section in snippets:
            if section['header'] == target_header:
                for pid, snippet in section.items():
                    if pid in target_pids: 
                        paragraphs.append({pid: clean_snippet(snippet)})
        return paragraphs
                 



    def get_movie_info(self, movie_id):
        return self.movie_infos[movie_id]

def get_movie_count(stages):
    count_movies = 0
    for header, stage in stages.items():
        count_movies += len(stage['movies'])
    return count_movies


def loadJson(filepath, map=lambda x: x):
    return map(json.load((open(filepath))))

def decideHeader(mentions):
    header_snippets_count = {}
    for section in mentions:
        header = section[0]['header']
        header_snippets_count[header] = len(section)

    return max(header_snippets_count, key=header_snippets_count.get)
def filter_snippets(header, snippets):
    res = [] 
    for section in snippets:
        for sentence in section:
            if sentence['header'] == header:
                res.append(sentence)
    return res

def clean_snippet(snippet):
    return re.sub("[\(\[].*?[\)\]]", "", snippet).strip()


