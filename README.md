# Notionfilms

This program extracts relevant information from imdb and watchmode and paste it in a database in Notion. The first part of program (peliculas.py) extract information from imdb with the library cinemagoer and from the watchmode API. The second part take that data and upload it in a Notion database using its official API.

The library cinemagoer is not working properly becouse sometimes it does not return all the information requested. I am currently working on fixing this error by extracting the data from another source or with another technology.

![image](https://user-images.githubusercontent.com/116549614/198663829-5b95724a-331f-489e-8a55-115ec5112176.png) 
![image](https://user-images.githubusercontent.com/116549614/198664882-73580e3a-0003-40eb-8ecd-cc4f3ae1c8b0.png)


## How to install and run the program
To run the program besides python you need:
- Install cinemagoer ($pip install cinemagoer)

- Download the database template in Notion: https://excellent-woodpecker-1c6.notion.site/26aca168771e4c77af01088f5d4be12a?v=667e7cb6d8e3462e92554f74bf400f84

- Notion integration: tutorial: https://www.codingwithmiszu.com/2021/12/28/how-to-generate-a-notion-api-token-easily/)

- Notion database ID:
  * If you enter to your database with Notion web the URL will be something like *https://www.notion.so/<long_hash_1>?v=<long_hash_2>*, where <long_hash_1> = ID

- Watchmode token: request your API token in https://api.watchmode.com/

**Finally insert the Notion token, Watchmode token and database ID in the main.py code.**

## How to use the program
1. You have to insert a new line for each film you want in the database with its name (english) and realese year (optional but recommendable)
2. Run the main.py program and watch if the the program find an imdb id for each film. The library cinemagoer is slow so the process could last few minutes if there are a lot of films.* 
3. The program should print something like this for each film:

![image](https://user-images.githubusercontent.com/116549614/198677464-e840757f-34f0-47e3-bcc1-721d875bf540.png)

*Now cinemagoer seems to be having some problems finding the imdb IDs, if it does not find all the imdb ID try to rerun the code. I am working on solving this problem.
