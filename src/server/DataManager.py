import json
from collections import defaultdict
from pprint import pprint
import re
from nltk import tokenize

class DataManager():
    def __init__(self):
        artist_infos = loadJson(r"data/target_actor_info.json")
        self.actor_info_dict = {x['id']: x for x in artist_infos}
        artist_images = loadJson(r"data/images.json")
        self.artist_image_dict = {x['id']: x['image'] for x in artist_images}
        self.movie_infos = loadJson(r"data/movie_pool.json")
        self.careers = loadJson(r"data/career_w_snippets.json")
        self.snippets_path = "data/career_snippets/"

    def loadCareer(self, artist_id):
        career = self.careers[artist_id]
        return self.preprocess_career(artist_id, self.add_infos(career))
    def loadInfo(self, artist_id):
        info = self.actor_info_dict[artist_id]
        if artist_id in self.artist_image_dict:
            image = self.artist_image_dict[artist_id] 
            info['image'] = image
        knownForIds = info['knownForTitles'].split(",")
        titles = []
        for id in knownForIds:
            print(id, self.movie_infos[id])
            if id in self.movie_infos:
                titles.append(self.movie_infos[id]['title'])
        info['knownTitles'] = titles

        return info

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
        stage_index = 0 
        header_list = []
        for movie_info in movie_infos:
            if not movie_info['snippet']: 
                empty_movies.append(movie_info)
                continue
            # create a stage 
            header = decideHeader(movie_info['snippet'], header_list)
            movie_info['snippet'] = filter_snippets(header, movie_info['snippet'])
            if header not in header_list:
                new_stage = {
                    "header": header,
                    "paragraphs": set(),
                    "movies": empty_movies,
                    "stage": stage_index
                }
                stage_index += 1
                stages[header] = new_stage
                cur_stage = header
                header_list.append(header)
            else:
                stages[cur_stage]['movies'] += empty_movies
            stages[header]['movies'].append(movie_info)
            empty_movies = []
            for sentence in movie_info['snippet']:
                paragraph = sentence['p']
                new_stage['paragraphs'].add(paragraph)

        if empty_movies and cur_stage != "":
            stages[cur_stage]["movies"] += empty_movies

        # post process
        stages_list = [None] * stage_index
        for header, stage in stages.items():
            stage['paragraphs'] = list(stage['paragraphs'])
            stage_index = stage['stage']
            paragraph_list = self.getParagraphs(artist_id, header, stage['paragraphs']) 
            for movie in stage['movies']:
                movie['stage'] = stage_index
                movie['snippet'] = add_sentence_index(movie['snippet'], paragraph_list)

            if header == "empty":
                min_year = min(list(map(lambda movie: movie['year'], stage['movies'])))
                max_year = max(list(map(lambda movie: movie['year'], stage['movies'])))
                header = min_year + " - " + max_year

            stages_list[stage_index] = {
                "header": header,
                "paragraphs": paragraph_list, 
                "movies": stage['movies']
            }
        return stages_list
        
    def getParagraphs(self, actor_id, target_header, target_pids):
        snippets = json.load(open(self.snippets_path + actor_id + ".json"))['career']
        paragraphs = []
        for section in snippets:
            if section['header'] == target_header:
                for pid, snippet in section.items():
                    if pid in target_pids: 
                        paragraphs.append({pid: splitSentences(snippet, post_process=clean_snippet)})
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

def decideHeader(mentions, header_list):
    header_snippets_count = {}
    for section in mentions:
        header = section[0]['header']
        if header not in header_list or header == header_list[len(header_list)-1]:
            header_snippets_count[header] = len(section)
    if not header_snippets_count: 
        return header_list[len(header_list)-1]
    else:
        return max(header_snippets_count, key=header_snippets_count.get)

def filter_snippets(header, snippets):
    res = [] 
    for section in snippets:
        for sentence in section:
            if sentence['header'] == header:
                res.append(sentence)
    return res

def add_sentence_index(sentences, paragraph_list):
    for sentence in sentences:
        for paragraph in paragraph_list:
            # paragraph_sentences = splitSentences(list(paragraph.values())[0], post_process=clean_snippet)
            for (index, paragraph_sentence) in enumerate(list(paragraph.values())[0]):
                if sentence['snippet'] == paragraph_sentence:
                    sentence['index'] = index
                    break
    return sentences


def clean_snippet(snippet):
    return re.sub("[\(\[].*?[\)\]]", "", snippet).strip()

def splitSentences(content, post_process=lambda x:x):
    return list(map(post_process, tokenize.sent_tokenize(content)))

