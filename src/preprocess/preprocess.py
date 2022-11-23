from ctypes import cast
import json
import csv
from collections import defaultdict
from pprint import pprint
import requests
from bs4 import BeautifulSoup
import sys
import datetime
import os
from os import listdir
from os.path import isfile, join
import glob
# csv.f_size_limit(sys.maxsize)
def main():
    if __name__ == '__main__':
        # movie_principals = tsv_to_dicts(r'principals.tsv') 
        # english_movie_ids = json.load(open(r'english_movie_ids.json'))
        # print('tt10872600' in english_movie_ids)
        # actor_names = tsv_to_dicts(r'name.tsv') 
        # actor_nid_dict = {x['nconst']: x for x in actor_names}
        # movie_infos = tsv_to_dicts(r'title_basics.tsv')
        # movie_id_dict = {x['tconst']: x for x in movie_infos}
        # print(movie_id_dict['tt10872600'])
        # print(len(movie_ids))
        # filtered_movies = filter_movie(movie_id_dict, english_movie_ids)
        # save_json(filtered_movies, r'filtered_movies.json')
        # kept_movies = json.load(open(r'merged_kept_movies.json'))
            
        # path = r'film_credits'
        # scraped_movie_ids = [f.split(".")[0] for f in listdir(path) if isfile(join(path, f))]
        # movie_ids = list(map(lambda movie: movie['tconst'], kept_movies))
        # resume = list(set(movie_ids) - set(scraped_movie_ids))
        # print(len(movie_ids))
        # movie_ids = ['tt0800080']
        # scrape_imdb_film_credits(resume)

        # movie_credits = []
        # for credit_file in glob.glob(r'film_credits_w_ids/*.json'):
        #     credits = json.load(open(credit_file))
        #     movie_credits.append(credits)

        # movie_subset_file = open(r'movie_subsets.txt')
        # subset_movie_ids = list(map(lambda id: id.strip(), movie_subset_file.readlines()))
        # actor_list = extract_actor_list_from_movie_subset(subset_movie_ids)
        # actor_careers = extract_actor_career(actor_list, movie_credits)
        # actor_info_list = json.load(open(r'target_actor_info.json'))
        # scrape_career(actor_list=actor_info_list)
        # generate_movie_pool()
        add_snippets()
        

def tsv_to_dicts(csvFilePath):
    #read csv file
    csvReader = None
    csvf = open(csvFilePath, encoding='utf-8')
        #load csv file data using csv library's dictionary reader
    csvReader = csv.DictReader(csvf, delimiter='\t', skipinitialspace=True) 
    return csvReader
    for row in csvReader: 
        #add this python dict to json array
        if(row['tconst'] == 'tt0496806'):
            pprint(row)

def save_json(data, filepath=r'new_dict.json'):
    with open(filepath, 'w') as fp:
        json.dump(data, fp, indent=4)

def scrape_imdb_film_credits(film_id_list):
    imdb_film_prefix = "https://www.imdb.com/title/"
    imdb_full_credit_suffix = "/fullcredits"
    count = 0
    movie_credits = []
    total_time = 0
    total_movies = len(film_id_list)
    t_previous = datetime.datetime.now()
    for id in film_id_list:
        url = imdb_film_prefix + id + imdb_full_credit_suffix 
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            cast_list = scrape_cast_list(soup)
            poster = scrape_poster(soup)
            director_list = scrape_simpleTable(soup, "director")
            writer_list = scrape_simpleTable(soup, "writer")
            producer_list = scrape_simpleTable(soup, "producer")

            film_credits = {
                "id": id,
                "poster": poster,
                "casts": cast_list,
                "directors": director_list,
                "writers": writer_list,
                "producers": producer_list
            }
            save_json(film_credits, "film_credits/" +id+".json")
            t_cur = datetime.datetime.now()
            total_time += (t_cur - t_previous).microseconds 
            t_previous = t_cur
            count += 1
            avg_time = total_time/count
            estimate_left_time = avg_time*(total_movies - count)/60/1000000
            print("{}/{}, {} minutes left".format(count, total_movies, estimate_left_time))
        else:
            print(response)

def scrape_poster(soup):
    try:
        img_tag = soup.find("img", attrs={"class": "poster"})
        img_src = img_tag.get("src")
        return img_src
    except Exception as e:
        return None


def scrape_cast_list(soup):
    try:
        cast_list_table = soup.find_all("table", attrs={"class": "cast_list"})
        if not cast_list_table:
            return None
        cast_list_table = cast_list_table[0].contents

        casts = []
        candidate_num = 0
        for cast_row in cast_list_table: 
            if cast_row == '\n': continue
            # print(cast_row)
            # print("--------------")
            if cast_row.has_attr('class'):
                cast = {
                    "rank": candidate_num + 1,
                }
                for info in cast_row.contents:
                    if info == '\n': continue
                    # image
                    if info.has_attr("class") and info['class'][0] == 'primary_photo':
                        img_tag = info.find("img")
                        if img_tag is None:
                            img_src = "None"
                        else:
                            img_src = img_tag.get('src')
                        cast['img'] = img_src
                    # actor name
                    if not info.has_attr("class"):
                        a_tag = info.find("a")
                        if a_tag is None:
                            actor_name = "None"
                        else:
                            actor_name = a_tag.text.strip()
                            src = a_tag.get('href')
                            if src is None:
                                actor_id = None
                            else:
                                actor_id = src.split("/")[2]
                        cast['name'] = actor_name
                        cast['id'] = actor_id
                    # character name
                    if info.has_attr("class") and info['class'][0] == 'character':
                        a_tag = info.find("a")
                        if a_tag is None:
                            character_name = "None"
                        else:
                            character_name = a_tag.text.strip()
                        cast['character'] = character_name
                casts.append(cast)
                candidate_num += 1
        return casts
        # movie_info = {
        #     "id": id,
        #     "top_casts": top_casts
        # }
        # save_json(movie_info, "movie_top_casts/" +id+".json")
        # movie_top_casts.append(movie_info)
    except Exception as e:
        return None


def scrape_simpleTable(soup, id):
    try:
        header =  soup.find("h4", attrs={"id": id})
        table = header.nextSibling.nextSibling
        rows = table.find_all("tr")
        credits = []
        for row in rows:
            tds = row.find_all("td")
            name = ""
            credit = ""
            for td in tds:
                if not td.has_attr("class"): continue
                if td['class'][0] == "name":
                    name = td.text.strip()
                if td['class'][0] == 'credit':
                    credit = td.text.strip()
            if name == "": continue
            credits.append({
                "name": name,
                "credit": credit
            })
        return credits
    except Exception as e:
        return None


# def scrape_actor_works(actor_id_list):
#     imdb_actor_prefix = "https://www.imdb.com/name/"
#     count = 0
#     exceptions = []
#     for id in actor_id_list:
#         count += 1
#         print("{}/{}".format(count, len(actor_id_list)))
#         url = imdb_actor_prefix + id
#         response = requests.get(url)
#         try:
#             if response.status_code == 200:
#                 soup = BeautifulSoup(response.content, 'html.parser')
#                 filmography_container = soup.find("div", attrs={"id": "filmography"})
#                 if not filmography_container:
#                     exceptions.append({
#                         "id": id,
#                         "exception": "no filmography available"
#                     })
#                     continue
#                 top_casts = []
#                 max_candidates = 15
#                 candidate_num = 0
#                 for cast_row in filmography_container.children: 
#                     if cast_row == '\n': continue

#                     print(cast_row)
#                     return
#                     if candidate_num >= max_candidates: break
#                     # print(cast_row)
#                     # print("--------------")
#                     if cast_row.has_attr('class'):
#                         cast = {
#                             "rank": candidate_num + 1,
#                         }
#                         for info in cast_row.contents:
#                             if info == '\n': continue
#                             # image
#                             if info.has_attr("class") and info['class'][0] == 'primary_photo':
#                                 img_tag = info.find("img")
#                                 if img_tag is None:
#                                     img_src = "None"
#                                 else:
#                                     img_src = img_tag.get('src')
#                                 cast['img'] = img_src
#                             # actor name
#                             if not info.has_attr("class"):
#                                 a_tag = info.find("a")
#                                 if a_tag is None:
#                                     actor_name = "None"
#                                 else:
#                                     actor_name = a_tag.text.strip()
#                                 cast['name'] = actor_name
#                             # character name
#                             if info.has_attr("class") and info['class'][0] == 'character':
#                                 a_tag = info.find("a")
#                                 if a_tag is None:
#                                     character_name = "None"
#                                 else:
#                                     character_name = a_tag.text.strip()
#                                 cast['character'] = character_name
#                         top_casts.append(cast)
#                         candidate_num += 1
#                 movie_info = {
#                     "id": id,
#                     "top_casts": top_casts
#                 }
#                 save_json(movie_info, "movie_top_casts/" +id+".json")
#                 # movie_top_casts.append(movie_info)
#         except Exception as e:
#             exceptions.append({
#                 "id": id,
#                 "exception": "unknown exception"
#             })
#         save_json(exceptions, "movie_top_casts_exceptions.json")



def filter_movie(movie_id_dict, english_movie_ids):
    kept = []
    count = 0
    genre_set = set()
    filtered_genres = ['Game-Show', 'Reality-TV', '\\N']
    for movie_id in english_movie_ids:
        count += 1
        if count % 1000 == 0:
            print(count, "/", len(english_movie_ids))
        if movie_id not in movie_id_dict.keys(): continue 
        movie = movie_id_dict[movie_id]
        if movie['tconst'] not in english_movie_ids: continue
        year = movie['startYear']
        title = movie['titleType']
        time = movie['runtimeMinutes']
        genres = movie['genres']
        # filter constraints
        if not genres: continue
        genres = genres.split(",")
        if not year.isdigit() or int(year) < int("1950"): continue
        if title != "movie": continue
        if not time.isdigit() or int(time) < int("90"): continue
        genre_check = [genre for genre in genres if genre in filtered_genres]
        if genre_check: continue
        genre_set.update(genres)
        kept.append(movie)
    i = 0
    for kept_movie in kept:
        i += 1
        if i % 1000 == 0:
            print(kept_movie)

    print(len(kept))
    save_json(kept, r'kept.json')
    return kept
    # save_json(genre_dict, r"genre_dict.json")

def extract_actor_list_from_movie_subset(movie_ids):
    actor_set = set()
    for movie_id in movie_ids:
        try:
            credits = json.load(open('film_credits/{}.json'.format(movie_id)))
            casts = credits['casts']
            if not casts: continue
            cast_ids = [cast['id'] for cast in casts]
            actor_set.update(cast_ids)
        except Exception as e:
            print(e)
            continue
    return list(actor_set)

def extract_actor_career(actor_list, movie_credits):
    actor_career_dict = {}
    progress = 0
    for movie in movie_credits:
        print(movie['id'])
        if movie['casts']:
            movie['casts'] = filter(lambda cast: 'id' in cast, movie['casts'])
            cast_ids = list(map(lambda cast: cast['id'], movie['casts']))
            check_credit(actor_list, cast_ids, "actor", actor_career_dict, movie['id'])
        if movie['directors']:
            movie['directors'] = filter(lambda director: 'id' in director, movie['directors'])
            director_ids = list(map(lambda director: director['id'], movie['directors']))
            check_credit(actor_list, director_ids, "director", actor_career_dict, movie['id'])
        if movie['writers']:
            movie['writers'] = filter(lambda writer: 'id' in writer, movie['writers'])
            writer_ids = list(map(lambda writer: writer['id'], movie['writers']))
            check_credit(actor_list, writer_ids, "writer", actor_career_dict, movie['id'])
        if movie['producers']:
            movie['producers'] = filter(lambda producer: 'id' in producer, movie['producers'])
            producer_ids = list(map(lambda producer: producer['id'], movie['producers']))
            check_credit(actor_list, producer_ids, "producer", actor_career_dict, movie['id'])
        progress += 1
        print("{}/{}".format(progress, len(movie_credits)))
    for actor_id, career in actor_career_dict.items():
        career['id'] = actor_id
        save_json(career, "careers/" + actor_id + ".json")

def check_credit(actor_list, checked_list, idf, actor_career_dict, movie_id):
    for actor_id in checked_list:
        if actor_id in actor_list:
            if actor_id not in actor_career_dict.keys():
                actor_career_dict[actor_id] = {
                    "actor": [],
                    "director": [],
                    "writer": [],
                    "producer": [],
                }
            actor_career_dict[actor_id][idf].append(movie_id)


    



def scrape_actor_works(actor_id_list):
    from contextlib import closing
    from selenium.webdriver import Firefox # pip install selenium
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as EC
    imdb_actor_prefix = "https://www.imdb.com/name/"
    count = 0
    exceptions = []
    for id in actor_id_list:
        count += 1
        print("{}/{}".format(count, len(actor_id_list)))
        url = imdb_actor_prefix + id
        print(url)
        # use firefox to get page with javascript generated content
        with closing(Firefox()) as driver:
            driver.get(url)
            headers = driver.find_elements(By.TAG_NAME, "h3")
            # credits = driver.find_element(By.XPATH, "//span[contains(text(), 'Credits')]")
            credits_found = False
            credit_span = None
            for header in headers:
                spans = header.find_elements(By.TAG_NAME, 'span')
                for span in spans:
                    if span.text == "Credits":
                        credit_span = span
                        credits_found = True
                        break
                if credits_found: break
            if not credits_found:
                print("credits not found")
                return
            print(credit_span)
            while(True):
                parent = credit_span.find_element(By.XPATH, "..")
                class_list = parent.get_attribute("class")
                print(class_list)
                if class_list == 'ipc-page-section': break

            return
            section_headers = filmography_container.find_elements("class", "head")
            click = False
            for header in section_headers:
                header_name = header.get_attribute("data-category")
                # don't need to click on first section
                if click:
                    header.click()
                else:
                    click = True
                # wait for the page to load
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "filmo-category-section"))
                )
                # store it to string variable
                page_source = driver.page_source

                soup = BeautifulSoup(page_source)
                expanded_section = soup.find("div", attrs={"class": "filmo-category-section"})
                for row in expanded_section.children:
                    film_id = row['id'].split('-')[1]
                    print(header_name, film_id)
                return

def add_simple_table_ids():
    names = tsv_to_dicts(r'name.tsv') 
    print("constructing dict...")
    name_id_dict = {name['primaryName']: name['nconst'] for name in names}
    print("construct dict done")
    movie_credits = []
    for credit_file in glob.glob(r'film_credits/*.json'):
        credits = json.load(open(credit_file))
        movie_credits.append(credits)
    
    for movie in movie_credits:
        if movie['directors']:
            for director in movie['directors']:
                if director['name'] in name_id_dict:
                    id = name_id_dict[director['name']]
                    director['id'] = id
        if movie['writers']:
            for writer in movie['writers']:
                if writer['name'] in name_id_dict:
                    id = name_id_dict[writer['name']]
                    writer['id'] = id
        if movie['producers']:
            for producer in movie['producers']:
                if producer['name'] in name_id_dict:
                    id = name_id_dict[producer['name']]
                    producer['id'] = id

        save_json(movie, 'film_credits_w_ids/' + movie['id'] + ".json")

def scrape_career(actor_list):
    import requests
    from bs4 import BeautifulSoup
    wiki_prefix = "https://en.wikipedia.org/wiki/"

    # artist_career_dict = {}
    discarded_artist = []
    count = 0
    for actor in actor_list:
        count += 1
        print("{}/{}".format(count, len(actor_list)))
        id = actor['id']
        name = actor['name']
        wiki_id = name.replace(" ", "_")
        url = wiki_prefix + wiki_id 
        response = requests.get(url)
        career_sections = []
        try:
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                headers = soup.find_all("span", attrs={"class": "mw-headline"})
                career_header = None
                for header in headers:
                    if "career" in header.text.lower():
                        career_header = header
                if career_header is None:
                    discarded_artist.append(
                        {
                            "id": id,
                            "name": name,
                            "reason": "No career section",
                        }
                    )
                    print("no career section", name)
                    continue
                next_sibling = career_header.parent.next_sibling.next_element
                while(True):
                    if next_sibling == "\n":
                        next_sibling = next_sibling.next_element
                    if next_sibling.name == "h3":
                        new_section = {}
                        section_header = next_sibling
                        header_content = section_header.find_all("span", attrs={"class": "mw-headline"})[0]
                        new_section = { "header": header_content.text}
                        career_sections.append(new_section)
                        p_count = 0
                        next_sibling = next_sibling.next_sibling
                    elif next_sibling.name == "p":
                        content = ''.join(next_sibling.strings)
                        if len(career_sections) == 0:
                            career_sections.append({"header": "empty"})
                        career_sections[len(career_sections)-1]['p' + str(p_count)] = content
                        p_count += 1
                        next_sibling = next_sibling.next_sibling
                    elif next_sibling.name == "h2":
                        break
                    else:
                        next_sibling = next_sibling.next_sibling
                # artist_career_dict[id]["career"] = career_sections
            else:
                discarded_artist.append(
                    {
                        "id": id,
                        "name": name,
                        "reason": "No wiki page"
                    }
                )
                print("no wiki page:", name)
                continue
        except: 
            discarded_artist.append(
                {
                    "id": id,
                    "name": name,
                    "reason": "Unknown Exception"
                }
            )
            print("exception:", name)
            continue
        career = {
            "id": id,
            "name": name,
            "career": career_sections
        }
        save_json(career, "career_snippets/" + id + ".json")
    save_json(discarded_artist, "discarded_artist.json")

def extract_target_actor_info():
    actor_list = json.load(open(r'target_actor_list.json'))
    print("constructing dict...")
    actor_names = tsv_to_dicts(r'name.tsv') 
    actor_nid_dict = {x['nconst']: x for x in actor_names}
    print("construct dict done")
    target_actor_id_name_list = []
    for actor_id in actor_list:
        if actor_id not in actor_nid_dict: continue
        actor_info = actor_nid_dict[actor_id]
        actor_id_name = {
            "id": actor_id,
            "name": actor_info['primaryName'],
            "birthYear": actor_info['birthYear'],
            "deathYear": actor_info['deathYear'],
            "primaryProfession": actor_info['primaryProfession'],
            "knownForTitles": actor_info['knownForTitles']
        }
        target_actor_id_name_list.append(actor_id_name)
    save_json(target_actor_id_name_list, r'target_actor_id_name_list.json')
    return

def generate_movie_pool():
    movie_pool = set()
    for actor_career_file in glob.glob(r'careers/*.json'):
        career = json.load(open(actor_career_file))
        asActor = career['actor']
        asDirector = career['director']
        asWriter = career['writer']
        asProducer = career['producer']
        movie_pool.update(asActor)
        movie_pool.update(asDirector)
        movie_pool.update(asWriter)
        movie_pool.update(asProducer)
    movie_pool = list(movie_pool)
    movie_basics = tsv_to_dicts(r'title_basics.tsv')
    movie_basics_dict = {x['tconst']: x for x in movie_basics}
    movie_ratings = tsv_to_dicts(r'title_ratings.tsv')
    movie_ratings_dict = {x['tconst']: x for x in movie_ratings}

    movie_info_dict = {}
    for movie_id in movie_pool:
        if movie_id not in movie_basics_dict or movie_id not in movie_ratings_dict: continue
        movie_basics = movie_basics_dict[movie_id]
        movie_ratings = movie_ratings_dict[movie_id]
        movie_info_dict[movie_id] = {
            "id": movie_id,
            "title": movie_basics['primaryTitle'],
            "votes": movie_ratings['numVotes'],
            "ratings": movie_ratings['averageRating'],
            "genre": movie_basics['genres'],
            "year": movie_basics['startYear'],
        }
    save_json(movie_info_dict, r'movie_pool.json')

def add_snippets():
    movie_pool = json.load(open(r'movie_pool.json'))
    res = {}
    for actor_career_file in glob.glob(r'careers/*.json'):
        actor_id = os.path.basename(actor_career_file).split(".")[0]
        try:
            snippets = json.load(open("career_snippets/" + actor_id + ".json"))
        except:
            continue
        career = json.load(open(actor_career_file))
        asActor = career['actor']
        asDirector = career['director']
        asWriter = career['writer']
        asProducer = career['producer']
        actor_career_dict = defaultdict(list)
        merge_movie_roles(actor_career_dict, asActor, "actor")
        merge_movie_roles(actor_career_dict, asDirector, "director")
        merge_movie_roles(actor_career_dict, asWriter, "writer")
        merge_movie_roles(actor_career_dict, asProducer, "producer")

        res[actor_id] = generate_movie_info_w_snippet(snippets, actor_career_dict, movie_pool)
    save_json(res, r'career_w_snippets.json')

def merge_movie_roles(actor_career_dict, movie_ids, idf):
    for movie_id in movie_ids:
        actor_career_dict[movie_id].append(idf)


def generate_movie_info_w_snippet(actor_snippets, actor_career_dict, movie_pool_dict):
    actor_id = actor_snippets['id']
    actor_name = actor_snippets['name']
    movie_infos = []
    movie_ids = list(actor_career_dict.keys())
    for movie_id in movie_ids:
        if movie_id not in movie_pool_dict: continue
        movie_info = {
            "tid": movie_id,
            "role": actor_career_dict[movie_id],
            "wiki_description": [],
        }
        movie_title = movie_pool_dict[movie_id]['title']
        for section in actor_snippets['career']:
            header = section['header']
            paragraphs = []
            for p, content in section.items():
                if p == "header": continue
                if movie_title.lower() in content.lower(): # alternative: only store sentences, not entire paragraph
                    paragraphs.append(content) 
            if len(paragraphs) != 0:
                movie_info['wiki_description'].append({"header": header, "paragraphs": paragraphs})
        movie_infos.append(movie_info)
    return movie_infos

main()



