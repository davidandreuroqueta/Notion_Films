import urllib.request
import json


class Film:
    def __init__(self, name, year):
        self.name = name
        self.id = None
        self.year = year
        self.title = None
        self.poster = None
        self.director = None
        self.director_photo = None
        self.rating = None
        self.plot = None
        self.cast = []
        self.genres = None
        self.sources = []


    def get_tmdb_id(self, key, language):
        # Using Watchmode searcher, searching in the proper language
        search_name = urllib.parse.quote_plus(self.name)
        try:
            with urllib.request.urlopen(f'https://api.themoviedb.org/3/search/movie?api_key={key}&language={language}&query={search_name}&page=1&include_adult=false&region=ES&year={str(self.year)}') as url:
                data = json.loads(url.read().decode())
        except Exception as e:
            return False, f'{self.name}: Error conecting to the API while searching: {e}'
        
        # Searching in english 
        if data['total_results'] == 0: 
            try:
                with urllib.request.urlopen(f'https://api.themoviedb.org/3/search/movie?api_key={key}&language=en-US&query={search_name}&page=1&include_adult=false&region=ES&year={str(self.year)}') as url:
                    data = json.loads(url.read().decode())
            except Exception as e:
                return False, f'{self.name}: Error conecting to the API while searching: {e}'
        
        # Get the first result
        if data['total_results'] > 0:
            self.id =data['results'][0]['id']
            self.title = data['results'][0]['original_title']
            return True, f'{self.name} -> id = {self.id} -> title: {self.title}'
        return False, f'{self.name}: Film not found'


    def get_details_and_crew(self, key, language):
        try:
            with urllib.request.urlopen(f'https://api.themoviedb.org/3/movie/{self.id}?api_key={key}&language={language}&append_to_response=credits') as url:
                data = json.loads(url.read().decode())
        except Exception as e:
            return False, f'Error conecting to the API while getting deteails and crew: {e}'

        if data['backdrop_path'] == None:
            backdrop_path = 'https://upload.wikimedia.org/wikipedia/commons/e/eb/Blank.jpg'
        else: 
            backdrop_path = 'http://image.tmdb.org/t/p/w500'+data['backdrop_path']

        if data['poster_path'] == None:
            poster_path = 'https://upload.wikimedia.org/wikipedia/commons/e/eb/Blank.jpg'
        else: 
            poster_path = 'http://image.tmdb.org/t/p/w500'+data['poster_path']
        
        self.poster = (backdrop_path, poster_path)
        self.year = int(data['release_date'][:4])
        self.plot = data['overview']
        self.genres = [gen['name'] for gen in data['genres']]

        # Director info
        for person in data['credits']['crew']:
            if person['job'] == 'Director':
                self.director = person['name']
                if person['profile_path'] == None:
                    profile_path = 'https://riverlegacy.org/wp-content/uploads/2021/07/blank-profile-photo.jpeg'
                else: 
                    profile_path = 'http://image.tmdb.org/t/p/w500'+person['profile_path']

                self.director_photo = profile_path
                break

        # Cast info
        for actor in data['credits']['cast'][:7]:
            if actor['profile_path'] == None:
                profile_path = 'https://riverlegacy.org/wp-content/uploads/2021/07/blank-profile-photo.jpeg'
            else: 
                profile_path = 'http://image.tmdb.org/t/p/w500'+actor['profile_path']

            self.cast.append((actor['name'], profile_path))
    
        return True, f'{self.name}: Details and crew updated'


    def get_sources(self, key, region):
        try:
            with urllib.request.urlopen(f'https://api.themoviedb.org/3/movie/{self.id}/watch/providers?api_key={key}&region=ES') as url:
                data = json.loads(url.read().decode())
        except Exception as e:
            return False, f'{self.name}: Error conecting to the API while getting sources: {e}'
        
        if region not in data['results']:
            return False, f'{self.name}: Not avialable in your region'

        if 'flatrate' in data['results'][region]:
            for platform in data['results'][region]['flatrate']:
                self.sources.append(platform['provider_name'])
            
        return True, f'{self.name}: Sources updated'
    

    def __str__(self):
        r = f"""{self.title}, ({self.year}), id: {self.id}'
            {'='*30}
            Poster {self.poster}
            Genres: {self.genres}
            Director: {self.director}, {self.director_photo}
            Rating {self.rating}
            Plot: {self.plot}
            Cast: {self.cast}
            Platforms: {self.sources}"""
        return r