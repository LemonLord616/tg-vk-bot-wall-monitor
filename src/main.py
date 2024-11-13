import os
import sys
import requests
from dotenv import load_dotenv

import vk

load_dotenv()

VK_API_KEY = os.getenv("VK_API")
TG_API_KEY = os.getenv("TG_API")
VK_GROUP_ID = os.getenv("VK_GROUP")

session = vk.getLongPollServer(VK_GROUP_ID, VK_API_KEY)

server = session["server"]
key = session["key"]
ts = session["ts"]

while True:
		event = vk.getSessionEvent(server, key, ts, wait=25)
		ts = event["ts"]
		print(event)


