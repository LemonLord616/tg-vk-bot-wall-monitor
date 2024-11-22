import os
import asyncio
import time
import utils
from dotenv import load_dotenv

from vk import vkStartPolling
from tg import telegramStartPolling, sendMessageInChat

load_dotenv()

TG_API = os.getenv("TG_API")
TG_URL = os.getenv("TG_URL")
TG_CHAT_ID = os.getenv("TG_CHAT_ID")
VK_API = os.getenv("VK_API")
VK_GROUP_ID = os.getenv("VK_GROUP_ID")
VK_VERSION = os.getenv("VK_VERSION")
VK_URL = os.getenv("VK_URL")


async def messageTemplate(data):
		return str(data)


async def onVkPost(update):
	await sendMessageInChat(
			url=TG_URL,
			api_key=TG_API,
			chat_id=TG_CHAT_ID,
			text=await messageTemplate(update))

async def run():

	task1 = asyncio.create_task(telegramStartPolling(
		url=TG_URL,
		api_key=TG_API))
	task2 = asyncio.create_task(vkStartPolling(
		url=VK_URL,
		group_id=VK_GROUP_ID,
		access_token=VK_API,
		v=VK_VERSION,
		onUpdate=onVkPost))

	await task1
	await task2

async def run_gather():
	return await asyncio.gather(
			telegramStartPolling(
				url=TG_URL,
				api_key=TG_API), 
			vkStartPolling(
				url=VK_URL,
				group_id=VK_GROUP_ID,
				access_token=VK_API,
				v=VK_VERSION,
				onUpdate=onVkPost))


async def main():
	while True:
		try:
			await run_gather()
			break
		except Exception as e:
			print(e)


asyncio.run(main())

