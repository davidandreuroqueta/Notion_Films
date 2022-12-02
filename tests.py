import requests
import os
from dotenv import load_dotenv
import json

load_dotenv()

token = os.getenv('NOTION_TOKEN')

url = "https://api.notion.com/v1/blocks/6ab46d9f-61de-43b7-a5a0-cd7059b0b5c2/children?page_size=100"

headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json",
    "Notion-Version": "2022-02-22"
}

response = requests.get(url, headers=headers)

r = response.json()
print(r)
print(len(r['results']))