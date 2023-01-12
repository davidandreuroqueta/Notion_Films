from peliculas import Film
from notion import NotionClient
import os
import json
from dotenv import load_dotenv
from csv import DictReader

# def new_filmpage(client, name):
    # film = Film(name)
    # res = client.create_page(film)
    # return res

def get_settings():   
    with open('./settings.json', 'r') as f:
        data = json.load(f)
        return data['settings'].values()
    
def set_settings(name, value):
    with open('./settings.json', 'r+') as f:
        data = json.load(f)
        data['settings'][name] = value
        f.seek(0)
        json.dump(data, f)
        f.truncate()
    
def ask_for(ini_quest, expl, instance, l = []):
    res = None
    print(l)
    print(len(l)==0, res in l)
    while not (len(l) == 0 or res in l):
        try:
            res = instance(input(ini_quest))
        except:
            print('Invalid answare. The response datatype is not correct.')
            continue
        if not (len(l) == 0 or res in l):
            print(expl)
    return instance(res)

def first_page(notion_token, databaseId, tmdb_key, language, region):
    print('#'*50 + '\n' +
          '#'*5 + f'{"NOTION_FILMS APP":^40}' + '#'*5 + '\n' +
          '#'*50 + '\n')
    
    first = ask_for('Do you want to change the settings (y/n): ', 'Response not valid. Answer "y", "yes", "n" or "no". ', str, ['n', 'no', 'y', 'yes'])

    if first.lower() in ('y', 'yes'):
        return second_page(notion_token, databaseId, tmdb_key, language, region)
    
def second_page(notion_token, databaseId, tmdb_key, language, region):
    print('The current options are: ' + '\n' + '\n' +
        'Notion token: ' + notion_token + '\n' +
        'Notion database ID: ' + databaseId + '\n' +
        'TMDB key: ' + tmdb_key + '\n' +
        'Language (ISO 639-1): ' + language + '\n' +
        'Region (Look for it in the TMDB doc): ' + region + '\n'+ '\n'+ '\n')
    
    print('Change:' + '\n' +
            '1) Notion token' + '\n' +
            '2) Notion database ID' + '\n' +
            '3) TMDB key' + '\n' +
            '4) Language' + '\n' +
            '5) Region' + '\n' +
            '6) GO BACK')
    
    dic_options = {k+1: v for k, v in enumerate(['notion_token', 'databaseId', 'tmdb_key', 'language', 'region'])}
    print(dic_options)
    
    option = ask_for('Choose an option: ', 'Option not valid. Must be a number between 1-6', int, [1,2,3,4,5,6])
    if option == 6:
        return first_page(notion_token, databaseId, tmdb_key, language, region)
    new_value = input('New value: ')
    sure = ask_for('Are you sure? (y/n)', 'Response not valid. Answer "y", "yes", "n" or "no". ', str, ['n', 'no', 'y', 'yes'])
    if sure in {'y', 'yes'}:
        set_settings(dic_options[option], new_value)
    else:
        second_page(notion_token, databaseId, tmdb_key, language, region)
    
    
    

def extract_films_list(client):
    db = client.read_database()
  
    films = []
    for film in db['results']:
        # In case the block is empty
        if film['properties']['Titulo']['title'][0]['plain_text'] == '':
            continue

        dic = {}
        dic['id'] = film['id']
        dic['name'] = film['properties']['Titulo']['title'][0]['plain_text']
        try:
            dic['year'] = film['properties']['Año']['number']
        except KeyError:
            dic['year'] = None
        try:
            dic['tmdb_id'] = film['properties']['TMDB_id']['rich_text'][0]['text']['content']
        except IndexError:
            dic['tmdb_id'] = None
        films.append(dic)
        
    return films

def update_filmpage(client, tmdb_key, film_dic, region, language):
    film = Film(film_dic['name'], film_dic['year'])

    if film_dic['tmdb_id'] != None:
        film.id = film_dic['tmdb_id']
        res = film.get_sources(tmdb_key, region)
        if res[0]:
            res = client.update_sources(film_dic['id'], film)
        return res

    res = film.get_tmdb_id(tmdb_key, language)
    print(res[1])
    if res[0]:
        res1 = film.get_details_and_crew(tmdb_key, language)
        res2 = film.get_sources(tmdb_key, region)
        content, atributes = client.update_all_page(film_dic['id'], film)
        return str(res1[1] + '\n' + res2[1] + '\n' + content + '\n' + atributes)
    return res[0]
    
   

if __name__ == '__main__':
    load_dotenv()

    # Read settings from json
    notion_token, databaseId, tmdb_key, language, region = get_settings()

    notion_token = os.getenv('NOTION_TOKEN')
    tmdb_key = os.getenv('TMDB_TOKEN')
    language = 'es-ES' #ISO 639-1
    region = 'ES' #https://developers.themoviedb.org/3/movies/get-movie-watch-providers
    databaseId = os.getenv('DATABASEID')

    headers = {
        "Accept": "application/json",
        "Notion-Version": "2022-02-22",
        "Authorization": f"Bearer {notion_token}"
    }
    
    first_page(notion_token, databaseId, tmdb_key, language, region)

        
    
    
    # client = NotionClient(notion_token, databaseId)
    # with open("films_info.csv", 'r') as f:
     
    #     dict_reader = DictReader(f)
        
    #     films_info = list(dict_reader)
    
    # # print(films_info)

    # # films_info = extract_films_list(client)

    # if len(films_info) > 0:
    #     for film_dic in films_info:
    #         print(film_dic)
    #         res = update_filmpage(client, tmdb_key, film_dic, region, language)
    #         print(res)
    #         print('\n')
    # else:
    #     print('No hay películas por actualizar')