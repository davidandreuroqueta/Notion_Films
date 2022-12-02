import requests, json
import datetime


class NotionClient:

    def __init__(self, token, database_id):
        self.database_id = database_id

        self.headers = {
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json",
            "Notion-Version": "2022-02-22"
        }

    # read
    def read_database(self):
        url_read = f"https://api.notion.com/v1/databases/{self.database_id}/query"
        
        date_time = datetime.datetime.now()

        filter = {
                "filter": {
                    
                    "and":[
                        {
                        "property": "Titulo",
                        "title": {
                            "is_not_empty": True
                            }
                    }, 
                        {"or": [
                        {
                            "property": "Ultima edición plataformas",
                            "date": {
                                "before": date_time.strftime("%Y-%m-%d")
                            }
                        },
                        {
                            "property": "Ultima edición plataformas",
                            "date": {
                                "is_empty": True
                                }
                        }
                        ]
                    }
                ]
            }
        }
            
        res = requests.post(url_read, json = filter, headers = self.headers)
        data = res.json()
        if res.status_code != 200:
            raise Exception(f'Error reading the pending films\n{res.text}')
        return data


    def cast_block(self, cast):
        block = {
            "object": "block",
            "type": "column_list",
            "column_list": {
                "children": [
                ]
            }
        }
        i = 0
        while i < len(cast):
            if cast[i][1] != None:
                actor, photo = cast[i]
            else:
                actor = cast[i][0]
                photo = "https://riverlegacy.org/wp-content/uploads/2021/07/blank-profile-photo.jpeg"
            
            actor_block = {
                "type": "column",
                "column": {
                    "children": [
                        {
                            "type": "image",
                            "image": {
                                "type": "external",
                                "external": {
                                    "url": photo
                                }
                            }
                        },
                        {
                            "type": "paragraph",
                            "paragraph": {
                                "rich_text": [{
                                    "type": "text",
                                    "text": {
                                        "content": actor,
                                    }
                                }]
                            }
                        }
                    ]
                }
            }
            block["column_list"]["children"].append(actor_block)
            i += 1
        return block

    # update page content
    def page_content(self, page_id, director, director_photo, cast, plot):
        url = f"https://api.notion.com/v1/blocks/{page_id}/children"
        # Eliminar el bloque antes de subir el otro, en algunos casos
        data = {"children": [
                    # Titulo
                    {
                        "heading_1": {
                            "color": "default",
                            "rich_text": [
                                {
                                    "plain_text": "Reparto",
                                    "text": {
                                        "content": "Reparto",
                                    },
                                    "type": "text"
                                }
                            ]
                        },
                        "object": "block",
                        "type": "heading_1"
                    },

                    # Reparto
                    self.cast_block(cast),

                    # Resumen y director
                    {
                        "type": "column_list",
                        "column_list": {
                            "children": [
                                {
                                    "type": "column",
                                    "column": {
                                        "children": [
                                            {
                                                "type": "heading_2",
                                                "heading_2": {
                                                    "rich_text": [{
                                                    "type": "text",
                                                    "text": {
                                                        "content": "Resumen",
                                                    }
                                                    }],
                                                    "color": "default"
                                                }
                                            },
                                            {
                                                "type": "paragraph",
                                                "paragraph": {
                                                    "rich_text": [{
                                                        "type": "text",
                                                        "text": {
                                                            "content": plot,
                                                        }
                                                    }],
                                                    "color": "default",
                                                }
                                            }
                                        ]
                                    }
                                },
                                {
                                    "type": "column",
                                    "column": {
                                        "children": [
                                            {
                                                "type": "image",
                                                "image": {
                                                    "type": "external",
                                                    "external": {
                                                        "url": director_photo
                                                    }
                                                }
                                            },
                                            {
                                                "type": "paragraph",
                                                "paragraph": {
                                                    "rich_text": [{
                                                        "type": "text",
                                                        "text": {
                                                            "content": director,
                                                        }
                                                    }]
                                                }
                                            }
                                        ]
                                    }
                                }
                            ]
                        }
                    },
                    {
                        "heading_2": {
                            "color": "default",
                            "rich_text": [
                                {
                                    "plain_text": "Opinion personal",
                                    "text": {
                                        "content": "Opinion personal",
                                    },
                                    "type": "text"
                                }
                            ]
                        },
                        "object": "block",
                        "type": "heading_2"
                    },
                    {
                        "object": "block",
                        "paragraph": {
                            "color": "default",
                        "rich_text": [
                            {
                                "plain_text": "Aqui va mi opinión",
                                "text": {
                                    "content": "Aqui va mi opinión",
                                },
                                "type": "text"
                            }
                        ]
                        }
                    }
                ]}

        res = requests.patch(url, json = data, headers=self.headers)
        return res

    # def create_page(self, film):
        create_url = 'https://api.notion.com/v1/pages'

        genero = [{"name": tag} for tag in film.genres]

        data = {
        "parent": { "database_id": self.database_id },
        "properties": {
            "Titulo": {
                "title": [
                    {
                        "text": {
                            "content": film.title
                        }
                    }
                ]
            },
            "Director": {
                "select": {
                        "name": film.director
                    }
            },
            "Generos": {
                "multi_select": genero
            },
            "Nota": {
                "number": film.rating
            },
            # "Plataforma": {
            #     "multi_select": plataforma
            # },
            "Imagen": {
                    "files": [
                    {
                        "name": "000150748673-ofnuhb-t500x500.jpg",
                        "type": "external",
                        "external": {
                        "url": film.poster,
                        }
                    }
                    ]
            },
            "Año": {
                "number": film.year
            },
            "children": self.page_content(1, film.director, film.director_photo, film.cast, film.plot)
            }
        }


        data = json.dumps(data)
        res = requests.post(create_url, headers=self.headers, data=data)
        print(res.status_code)
        if res.status_code != 200:
            print(res.content)
        return res

    # update page information
    def update_all_page(self, pageId, film):
        """
        This method update the page to insert all the information of the movie.
        """
        update_url = f"https://api.notion.com/v1/pages/{pageId}"

        date_time = datetime.datetime.now()
        gendres = [{"name": tag} for tag in film.genres]
        sources = [{"name": tag} for tag in film.sources]

        data = {
        "parent": { "database_id": self.database_id },
        "properties": {
            "Titulo": {
                "title": [
                    {
                        "text": {
                            "content": film.title
                        }
                    }
                ]
            },
            "Año":{
                "number": film.year
            },
            "Director": {
                "select": {
                        "name": film.director
                    }
            },
            "Generos": {
                "multi_select": gendres
            },
            "Nota": {
                "number": film.rating
            },
            "Plataformas": {
                "multi_select": sources
            },
            "Imagen": {
                    "files": [
                    {
                        "name": "Portada",
                        "type": "external",
                        "external": {
                        "url": film.poster[0],
                        }
                    },
                    {
                        "name": "Cartel",
                        "type": "external",
                        "external": {
                        "url": film.poster[1],
                        }
                    }
                    ]
            },
            "TMDB_id": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                        "content": str(film.id)
                        }
                    }]
            },
            "Ultima edición plataformas":{
                "date": {
                    "start": date_time.strftime("%Y-%m-%d")
                    }
            }
            }
        }

        data = json.dumps(data)

        # update page content
        res2 = self.page_content(pageId, film.director, film.director_photo, film.cast, film.plot)
        if res2.status_code  == 200:
            content = f'{film.name}: Content updated in Notion'
        else: 
            raise Exception(f'{film.name}: Error updating content in Notion \n{res2.content}')
        
        # update page info
        res1 = requests.patch(update_url, headers=self.headers, data=data)
        if res1.status_code == 200:
            atributes = f'{film.name}: Attributes updated in Notion'
        else:
            raise Exception(f'{film.name}: Error updating attributes in Notion\n{res1.content}')
        
        return content, atributes
    
    def update_sources(self, pageId, film): 
        update_url = f"https://api.notion.com/v1/pages/{pageId}"

        date_time = datetime.datetime.now()
        sources = [{"name": tag} for tag in film.sources]

        data = {
        "parent": { "database_id": self.database_id },
        "properties": {
            "Plataformas": {
                "multi_select": sources
            },
            "Ultima edición plataformas":{
                "date": {
                    "start": date_time.strftime("%Y-%m-%d")
                    }
            }
        }
        }
        data = json.dumps(data)

        res = requests.patch(update_url, headers=self.headers, data=data)
        if res.status_code == 200:
            return f'{film.name}: Sources updated'
        else:
            raise Exception(f'{film.name}: Error updating sources in Notion\n{res.content}')
        