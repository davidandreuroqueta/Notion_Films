# Notionfilms

This program extracts relevant information from imdb and watchmode and paste it in a database in Notion. The first part of program (peliculas.py) extract information from imdb with the library cinemagoer and from the watchmode API. The second part take that data and upload it in a Notion database using its official API.

Furthermore, the sources of a film get updated when it has passed a day since the last update.

![image](https://user-images.githubusercontent.com/116549614/215763800-f34818df-7b93-4cb2-84a7-27e0bd58ca4e.png)
![image](https://user-images.githubusercontent.com/116549614/215764336-50a3522c-50f0-4472-9d12-7f668270e1dd.png)

## How to install and run the program
To run the program besides python you need:

- Download the database template in Notion: https://excellent-woodpecker-1c6.notion.site/26aca168771e4c77af01088f5d4be12a?v=667e7cb6d8e3462e92554f74bf400f84

- Notion integration: tutorial: https://www.codingwithmiszu.com/2021/12/28/how-to-generate-a-notion-api-token-easily/)

- Notion database ID:
  * If you enter to your database with Notion web the URL will be something like *https://www.notion.so/<long_hash_1>?v=<long_hash_2>*, where <long_hash_1> = ID

- Watchmode token: request your API token in https://api.watchmode.com/

**Finally insert the Notion token, Watchmode token, database ID, language and region in settings.json code.**

## How to use the program
1. You have to insert a new line for each film you want in the database with its name (selected language or english) and realese year.
2. Run the main.py program and watch if the film that finds is the one you want. 
3. The program should print something like this for each film:

![image](https://user-images.githubusercontent.com/116549614/215762494-41049b37-547b-4591-909a-2c41a38bbb7b.jpg)

![image (1)](https://user-images.githubusercontent.com/116549614/215762691-5a0d8661-2906-4b87-ba4e-5df968ac6a7f.jpg)
