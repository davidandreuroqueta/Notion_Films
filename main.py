from peliculas import Film
from notion import NotionClient
import os
from dotenv import load_dotenv

load_dotenv()

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

# def new_filmpage(client, name):
    # film = Film(name)
    # res = client.create_page(film)
    # return res

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
        except KeyError:
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
    
   


client = NotionClient(notion_token, databaseId)

films_info = extract_films_list(client)
print(films_info)
# with open("peliculas.csv", "w"):
#     for 

if len(films_info) > 0:
    for film_dic in films_info:
        print(film_dic)
        res = update_filmpage(client, tmdb_key, film_dic, region, language)
        print(res)
        break
        res = update_filmpage(client, dic)
        print('\n')
else:
    print('No hay películas por actualizar')