import os
import sys
import requests
from dotenv import load_dotenv


load_dotenv()

VK_API_KEY = os.getenv("VK_API")
TG_API_KEY = os.getenv("TG_API")
VK_GROUP_ID = os.getenv("VK_GROUP")

params = {
        "group_id": f'{VK_GROUP_ID}',
        "access_token": VK_API_KEY,
        "v": "5.199"
}

response = requests.get("https://api.vk.com/method/groups.getById", params=params)

if response.status_code != 200:
        print("Failed to fetch data:", response.status_code)
        sys.exit()

data = response.json()

if "response" not in data:
        print("Error:", data.get("error", {}).get("error_msg", "Unknown error"))
        sys.exit()

print(data)
#for post in data["response"]["items"]:
#        print(f'Post ID: {post["id"]}, Text: {post["text"]}')

