import json
import csv
from collections import defaultdict
from pprint import pprint
import requests
from bs4 import BeautifulSoup

def main():
    if __name__ == '__main__':
        # movie_principals = tsv_to_dicts(r'principals.tsv') 
        # actor_names = tsv_to_dicts(r'name.tsv') 
        # actor_nid_dict = {x['nconst']: x for x in actor_names}
        # movie_infos = tsv_to_dicts(r'basics.tsv')

        # movie_ids = list(map(lambda movie: movie['tconst'], movie_infos))
        # movie_ids = ['tt0000002', 'tt0000003', 'tt0000004','tt0000006','tt0000007','tt0000010','tt0000011']
        # movie_ids = ['tt0000007']
        # scrape_imdb_film_cast(movie_ids)
        # actor_ids = ['tt0000002', 'tt0000003', 'tt0000004','tt0000006','tt0000007','tt0000010','tt0000011']
        actor_ids = ['nm0000199']
        scrape_actor_works(actor_ids)


        # find = False
        # for principal_row in movie_principals:
        #     if(principal_row['tconst'] == 'tt0496806'):
        #         nconst = principal_row['nconst']
        #         print(actor_nid_dict[nconst])
        #         find=True
        #     elif find:
        #         return
                



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

def scrape_imdb_film_cast(film_id_list):
    imdb_film_prefix = "https://www.imdb.com/title/"
    imdb_full_credit_suffix = "/fullcredits"
    count = 0
    movie_top_casts = []
    exceptions = []
    for id in film_id_list:
        count += 1
        print("{}/{}".format(count, len(film_id_list)))
        url = imdb_film_prefix + id + imdb_full_credit_suffix 
        response = requests.get(url)
        try:
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                cast_list_table = soup.find_all("table", attrs={"class": "cast_list"})
                if not cast_list_table:
                    exceptions.append({
                        "id": id,
                        "exception": "no cast list available"
                    })
                    continue
                cast_list_table = cast_list_table[0].contents

                top_casts = []
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
                                cast['name'] = actor_name
                            # character name
                            if info.has_attr("class") and info['class'][0] == 'character':
                                a_tag = info.find("a")
                                if a_tag is None:
                                    character_name = "None"
                                else:
                                    character_name = a_tag.text.strip()
                                cast['character'] = character_name
                        top_casts.append(cast)
                        candidate_num += 1
                movie_info = {
                    "id": id,
                    "top_casts": top_casts
                }
                save_json(movie_info, "movie_top_casts/" +id+".json")
                # movie_top_casts.append(movie_info)
        except Exception as e:
            exceptions.append({
                "id": id,
                "exception": "unknown exception"
            })
        save_json(exceptions, "movie_top_casts_exceptions.json")

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



def filter_movie(movie_list):
    kept = []
    kept_2 = []
    kept_3 = []
    kept_4 = []
    count = 0
    for movie in movie_list:
        # if movie['tconst'] == 'tt1210166':
        #     print(movie)
        #     break
        count += 1
        if count % 1000 == 0:
            print(count)
        year = movie['startYear']
        time = movie['runtimeMinutes']
        if year > "1950" and time > "60":
            kept.append(movie)
        if year > "1950" and time > "70":
            kept_2.append(movie)
        if year > "1950" and time > "80":
            kept_3.append(movie)
        if year > "1950" and time > "90":
            kept_4.append(movie)
    print(len(kept))
    print(len(kept_2))
    print(len(kept_3))
    print(len(kept_4))
    return movie

def scrape_actor_works(actor_id_list):
    from contextlib import closing
    from selenium.webdriver import Chrome # pip install selenium
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
        with closing(Chrome()) as driver:
            driver.get(url)
            filmography_container = driver.find_element("id", "filmography")
            if not filmography_container:
                exceptions.append({
                    "id": id,
                    "exception": "no filmography available"
                })
                continue
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

def add_artist_work_description(
    artist_works_dict_path=r'artist_works_dict.json', 
    artist_careers_path=r'careers/',
    movie_titles_path=r'titles.json',
):
    artist_dict = json.load(open(artist_works_dict_path))
    movie_list = json.load(open(movie_titles_path))
    movie_dict = {movie['id']: movie for movie in movie_list}
    count = 0

    artist_works_w_description_dict = defaultdict(list)
    for artist_id, works in artist_dict.items(): 
        count += 1
        artist_career_filepath = artist_careers_path + artist_id + "_career.json"
        try:
            career = json.load(open(artist_career_filepath))
        except:
            continue
        artist_works_w_description_dict[artist_id] = works
        for work in works:
            movie_id = work["id"]
            movie_title = movie_dict[movie_id]['title']
            work['wiki_description'] = []
            for section in career['career']:
                header = section['header']
                paragraphs = []
                for p, content in section.items():
                    if p == "header": continue
                    if movie_title.lower() in content.lower(): # alternative: only store sentences, not entire paragraph
                        paragraphs.append(content) 
                if len(paragraphs) != 0:
                    work['wiki_description'].append({"header": header, "paragraphs": paragraphs})
        print(artist_id, "{}/{}".format(count, len(artist_dict.keys())))
    
    save_json(artist_works_w_description_dict, r'artist_works_w_description.json')

main()



