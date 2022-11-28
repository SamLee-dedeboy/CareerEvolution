from ctypes import cast
import json
import csv
from collections import defaultdict
from pprint import pprint
import requests
from bs4 import BeautifulSoup
import sys
import datetime
from os import listdir
from os.path import isfile, join
import glob
import pandas
import numpy as np
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
        # for credit_file in glob.glob(r'film_credits/*.json'):
        #     credits = json.load(open(credit_file))
        #     movie_credits.append(credits)

        # movie_subset_file = open(r'movie_subsets.txt')
        # subset_movie_ids = list(map(lambda id: id.strip(), movie_subset_file.readlines()))
        # actor_list = extract_actor_list_from_movie_subset(subset_movie_ids)
        save_movie_subset()
        # print(actor_list)
        # extract_actor_name("tttes")
        # I'm working on this now
        # actor_careers = extract_actor_career(actor_list, movie_credits)
        

def extract_actor_name(name_ids):
    with open("imdb/name_basics.tsv") as file:
        tsv_file = csv.reader(file, delimiter="\t")
        for line in tsv_file:
            print(line)

def save_movie_subset():
    HP = {}
    HP_tmp = {}
    # # HP
    # movie_ids = ["tt0241527", "tt0295297", "tt0304141", "tt0330373", "tt0373889", "tt0417741", "tt0926084", "tt1201607"]
    # year_start = 2001
    # year_end = 2011
    # # Marvel 
    # movie_ids = ["tt0371746", "tt1228705", "tt1300854", "tt0800080", "tt0800369", "tt1981115", "tt3501632", "tt10648342", 
    #              "tt0458339", "tt1843866", "tt3498820", "tt0848228", "tt2395427", "tt4154756", "tt4154796", "tt2015381", 
    #              "tt3896198", "tt0478970", "tt5095030", "tt1211837", "tt9419884", "tt2250912", "tt6320628", "tt10872600", 
    #              "tt1825683", "tt9114286", "tt4154664", "tt3480822", "tt9376612", "tt9032400"]
    # year_start = 2008
    # year_end = 2022
    # # JamesB
    # movie_ids = ["tt0113189", "tt0120347", "tt0143145", "tt0246460", "tt0381061", "tt0830515", "tt1074638", "tt2379713", "tt2382320"]
    # year_start = 1995
    # year_end = 2021
    # # StarWars
    # movie_ids = ["tt0120915", "tt0121765", "tt0121766", "tt2488496", "tt2527336", "tt2527338", "tt3748528", "tt3778644"]
    # year_start = 1999
    # year_end = 2019
    # # Xmen
    # movie_ids = ["tt0120903", "tt0290334", "tt0376994", "tt0458525", "tt1270798", "tt1430132", "tt1877832", "tt1431045", 
    #              "tt3385516", "tt3315342", "tt5463162", "tt6565702", "tt4682266"]
    # year_start = 2000
    # year_end = 2020
    # LoR
    movie_ids = ["tt0120737", "tt0167261", "tt0167260", "tt0903624", "tt1170358", "tt2310332"]
    year_start = 2001
    year_end = 2014

    for movie_id in movie_ids:
        try:
            credits = json.load(open('film_credits_w_ids/{}.json'.format(movie_id)))
            casts = credits['casts']
            if (not casts): continue
            # get overall highest rank.
            for cast in casts:
                try:
                    # if cast['rank'] > 5:  break
                    if cast['id'] in HP_tmp.keys(): 
                        HP_tmp[cast['id']]['rank_accu'] += cast['rank']
                        HP_tmp[cast['id']]['count'] += 1
                    else:
                        # cast_id = cast['id']
                        HP_tmp[cast['id']] = {}
                        HP_tmp[cast['id']]['id'] = cast['id']
                        HP_tmp[cast['id']]['name'] = cast['name']
                        HP_tmp[cast['id']]['rank_accu'] = cast['rank']
                        HP_tmp[cast['id']]['count'] = 1
                    # print(cast['rank'], cast['name'])
                except Exception as e:
                    print(e)
                    continue
            # print(HP_tmp)

        except Exception as e:
            print(e)
            continue
    # print(HP_tmp)

    avg_rank = 60
    for movie_id in movie_ids:
        try:
            credits = json.load(open('film_credits_w_ids/{}.json'.format(movie_id)))
            casts = credits['casts']
            directors = credits['directors']
            writers = credits['writers']
            producers = credits['producers']
            if (not casts) and (not directors) and (not writers) and (not producers): continue

            for cast_key in HP_tmp:
                try:
                    cast = HP_tmp[cast_key]
                    if cast['count'] < len(movie_ids)-2:  continue
                    if cast['rank_accu']/cast['count'] > avg_rank:  continue
                    if cast['id'] in HP.keys(): continue
                    cast_id = cast['id']
                    HP[cast_id] = {}
                    HP[cast_id]['id'] = cast_id
                    HP[cast_id]['name'] = cast['name']
                    HP[cast_id]['role'] = "actor"
                    # print(cast['rank_accu']/cast['count'], cast['name'])
                except Exception as e:
                    print(e)
                    continue

            # for cast in casts:
            #     try:
            #         if cast['rank'] > 5:  break
            #         if cast['id'] in HP.keys(): continue
            #         cast_id = cast['id']
            #         HP[cast_id] = {}
            #         HP[cast_id]['id'] = cast_id
            #         HP[cast_id]['name'] = cast['name']
            #         print(cast['rank'], cast['name'])
            #     except Exception as e:
            #         print(e)
            #         continue
            for cast in directors:
                try:
                    if cast['id'] in HP.keys(): continue
                    cast_id = cast['id']
                    HP[cast_id] = {}
                    HP[cast_id]['id'] = cast_id
                    HP[cast_id]['name'] = cast['name']
                    HP[cast_id]['role'] = "director"
                    # print("director: ", cast['name'])
                except Exception as e:
                    print(e)
                    continue
            for cast in writers:
                try:
                    if cast['id'] in HP.keys(): continue
                    cast_id = cast['id']
                    HP[cast_id] = {}
                    HP[cast_id]['id'] = cast_id
                    HP[cast_id]['name'] = cast['name']
                    HP[cast_id]['role'] = "writer"
                    # print("writer: ", cast['name'])
                except Exception as e:
                    print(e)
                    continue
            for cast in producers:
                try:
                    if cast['id'] in HP.keys(): continue
                    if cast['credit'].split(' ')[0] != "producer":  continue
                    cast_id = cast['id']
                    HP[cast_id] = {}
                    HP[cast_id]['id'] = cast_id
                    HP[cast_id]['name'] = cast['name']
                    HP[cast_id]['role'] = "producer"
                    # print(cast['credit'], cast['name'])
                except Exception as e:
                    print(e)
                    continue
        except Exception as e:
            print(e)
            continue
    # print(len(HP.keys()), HP)

    # read title_ratings(get rating & popularity), title_basics(get movie name & year)
    movie_ratings = {}
    with open("imdb/title_ratings.tsv") as file:
        tsv_file = csv.reader(file, delimiter="\t")
        line_count = 0
        for line in tsv_file:
            if line_count==0: 
                line_count += 1
                continue
            movie_ratings[line[0]] = [float(line[1]), float(line[2])] # rating, vote
    # print(movie_ratings)
    movie_basics = {}
    with open("imdb/title_basics.tsv") as file:
        tsv_file = csv.reader(file, delimiter="\t")
        line_count = 0
        for line in tsv_file:
            if line_count==0: 
                line_count += 1
                continue
            if line[1] != "movie": continue
            if line[5] == '\\N': continue
            movie_basics[line[0]] = [line[3], int(line[5])] # name, year     
    # print(movie_basics)

    print(HP)
    pop_min = 1000000000000000
    pop_max = -1
    delete_list = []
    keep_list = []
    for ppl in HP.keys():
        # HP[ppl]['rate'] = np.zeros((year_end - year_start + 1))
        # HP[ppl]['vote'] = np.zeros((year_end - year_start + 1))
        HP[ppl]['movie_count'] = np.zeros((year_end - year_start + 1))
        HP[ppl]['popularity'] = np.zeros((year_end - year_start + 1))
        HP[ppl]['popularity_max'] = np.zeros((year_end - year_start + 1))
        HP[ppl]['pop_bin'] = np.zeros((year_end - year_start + 1))
        HP[ppl]['movie_name'] = np.zeros((year_end - year_start + 1))
        HP[ppl]['movie_name'] = list(HP[ppl]['movie_name'])
        ppl_movies = []
        actor_movie_list = {}
        try:
            actor_movie_list = json.load(open('actor_careers/{}.json'.format(ppl)))
        except Exception as e:
            print(e, HP[ppl]['name'], HP[ppl]['role'])
            delete_list.append(ppl)
            continue

        print(ppl)
        for role in actor_movie_list.keys():
            if role == "id": continue
            for movie in actor_movie_list[role]:
                ppl_movies.append(movie)
                if movie_basics[movie][1] <= year_end and movie_basics[movie][1] >= year_start:
                    # HP[ppl]['rate'][movie_basics[movie][1] - year_start] += movie_ratings[movie][0]
                    # HP[ppl]['vote'][movie_basics[movie][1] - year_start] += movie_ratings[movie][1]
                    popular = movie_ratings[movie][0]*movie_ratings[movie][1]
                    year_idx = movie_basics[movie][1] - year_start
                    m_name = movie_basics[movie][0]
                    # print(pop_min, pop_max, popular, year_idx, HP[ppl]['popularity_max'])

                    HP[ppl]['popularity'][year_idx] += popular
                    if popular > HP[ppl]['popularity_max'][year_idx]:
                        HP[ppl]['popularity_max'][year_idx] = popular
                        HP[ppl]['movie_name'][year_idx] = m_name
                    HP[ppl]['movie_count'][year_idx] += 1
                    HP[ppl]['pop_bin'][year_idx] = HP[ppl]['popularity_max'][year_idx]
                    # HP[ppl]['pop_bin'][movie_basics[movie][1] - year_start] = float(HP[ppl]['popularity'][movie_basics[movie][1] - year_start]/HP[ppl]['movie_count'][movie_basics[movie][1] - year_start])
                    # print(HP[ppl]['pop_bin'][movie_basics[movie][1] - year_start])
        
        if HP[ppl]['movie_count'][0] == 0: # must have works by the start year of the subset.
            delete_list.append(ppl)
            # HP[ppl]['movie_count'][0] = 1
        else:
            for tmp in range(year_end - year_start + 1):
                if HP[ppl]['movie_count'][tmp]!=0:
                    keep_list.append(HP[ppl]['pop_bin'][tmp])
            

        # if max(HP[ppl]['pop_bin']) > pop_max: 
        #     pop_max = max(HP[ppl]['pop_bin'])
        #     print("pop_max: ", pop_max)
        # if min(HP[ppl]['pop_bin']) < pop_min: 
        #     pop_min = min(HP[ppl]['pop_bin'])
        #     print("pop_min: ", pop_min)

    for ppl in delete_list:
        HP.pop(ppl, None)
    pop_max = max(keep_list)
    pop_min = min(keep_list)

    for ppl in HP.keys():
        try:
            # print(ppl, HP[ppl]['name'], HP[ppl]['popularity'], HP[ppl]['pop_bin'])
            # print(pop_min, pop_max, HP[ppl]['pop_bin'])
            for pop_idx in range(year_end - year_start + 1):
                # HP[ppl]['pop_bin'][pop_idx] = int((HP[ppl]['pop_bin'][pop_idx]-pop_min)*5 / (pop_max-pop_min)) # 0~5
                
                if HP[ppl]['movie_count'][pop_idx] != 0:
                    HP[ppl]['pop_bin'][pop_idx] = int((HP[ppl]['pop_bin'][pop_idx]-pop_min)*5 / (pop_max-pop_min)) # 0~5
                else:
                    HP[ppl]['pop_bin'][pop_idx] = HP[ppl]['pop_bin'][pop_idx-1]
            
            HP[ppl]['movie_count'] = list(HP[ppl]['movie_count'])
            HP[ppl]['popularity'] = list(HP[ppl]['popularity'])
            HP[ppl]['popularity_max'] = list(HP[ppl]['popularity_max'])
            HP[ppl]['pop_bin'] = list(HP[ppl]['pop_bin'])

            print(ppl, HP[ppl]['name'], HP[ppl]['movie_count'], HP[ppl]['pop_bin'])
        except Exception as e:
            print(e)
            continue
    # print(len(HP.keys()), HP)

    with open('LoR_{}.json'.format(avg_rank), 'w') as f:
        json.dump(HP, f)

    return

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

def extract_actor_career(actor_list, movie_credits):
    actor_career_dict = {}
    for movie in movie_credits:
        cast_ids = list(map(lambda cast: cast['id'], movie['casts']))
        director_ids = list(map(lambda cast: cast['id'], movie['directors']))
        writer_ids = list(map(lambda cast: cast['id'], movie['writers']))
        producer_ids = list(map(lambda cast: cast['id'], movie['producers']))


    return

    



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

main()



