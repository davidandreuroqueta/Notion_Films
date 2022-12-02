from main import extract_films_list
from notion import NotionClient
import os
from dotenv import load_dotenv
import csv

load_dotenv()

notion_token = os.getenv('NOTION_TOKEN')

databaseId = os.getenv('DATABASEID')


client = NotionClient(notion_token, databaseId)

films_info = extract_films_list(client)

with open('films_info.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=list(films_info[0].keys()))
    writer.writeheader()
    writer.writerows(films_info)