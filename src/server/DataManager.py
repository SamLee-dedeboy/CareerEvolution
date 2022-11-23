import json
class DataManager():
    def __init__(self):
        self.artist_infos = loadJson(r"data/target_actor_info.json")
        self.movie_infos = loadJson(r"data/movie_pool.json")
        self.careers = loadJson(r"data/career_w_snippets.json")

    def loadCareer(self, artist_id):
        career = self.careers[artist_id]
        return self.add_infos(career)

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
                "votes": movie_info['votes'],
                "rating": movie_info['ratings'],
                "genre": movie_info['genre'],
                "year": movie_info['year'],
                "role": role,
                "snippet": movie_snippet,
            })
        return movie_infos


    def get_movie_info(self, movie_id):
        return self.movie_infos[movie_id]



def loadJson(filepath, map=lambda x: x):
    return map(json.load((open(filepath))))



