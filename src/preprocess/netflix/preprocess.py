import json
import csv
from collections import defaultdict
from pprint import pprint

def preprocess_raw():
    csvFilePath = r'titles.csv'
    jsonFilePath = r'titles.json'
    csv_to_json(csvFilePath, jsonFilePath, lambda x: x)
    csvFilePath = r'credits.csv'
    jsonFilePath = r'credits.json'
    csv_to_json(csvFilePath, jsonFilePath, lambda x: x)

def csv_to_json(csvFilePath, jsonFilePath, preprocess_func):
    jsonArray = []
      
    #read csv file
    with open(csvFilePath, encoding='utf-8') as csvf: 
        #load csv file data using csv library's dictionary reader
        csvReader = csv.DictReader(csvf) 

        #convert each csv row into python dict
        for row in csvReader: 
            #add this python dict to json array
            jsonArray.append(row)
    
    preprocess_data = preprocess_func(jsonArray)
    #convert python jsonArray to JSON String and write to file
    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf: 

        jsonString = json.dumps(preprocess_data, indent=4)
        jsonf.write(jsonString)

def save_json(data, filepath=r'new_dict.json'):
    with open(filepath, 'w') as fp:
        json.dump(data, fp, indent=4)

def group_artist_works(filepath=r'credits.json'):

    data = json.load(open(filepath))
    artist_work_dict = defaultdict(list)
    artist_name_dict = defaultdict(list)
    for work in data:
        artist_id = work['person_id']
        artist_name = work['name']
        artist_character = work['character']
        artist_role = work['role']
        work_id = work['id']
        artist_work_dict[artist_id].append(
            {
                "id": work_id,
                "character": artist_character,
                "role": artist_role,
            }
        )
        artist_name_dict[artist_id] = artist_name
    # save_json(artist_work_dict, "artist_works_dict.json")
    save_json(artist_name_dict, "artist_name_dict.json")

def scrape_career(artist_name_path=r'artist_name_dict.json'):
    import requests
    from bs4 import BeautifulSoup
    wiki_prefix = "https://en.wikipedia.org/wiki/"
    artist_dict = json.load(open(artist_name_path))
    # artist_career_dict = {}
    discarded_artist = []
    count = 0
    for id, name in artist_dict.items():
        count += 1
        print("{}/{}".format(count, len(artist_dict.keys())))
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
        save_json(career, "careers/" +id+"_career.json")
    save_json(discarded_artist, "discarded_artist.json")

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




