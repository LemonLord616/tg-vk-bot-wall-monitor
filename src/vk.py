import utils


def handleResponseStatus(status):
	if status != 200:
		raise Exception(f'Error: {status}')


@utils.async_session(handleResponseStatus)
def getLongPollServer(*,
			  url: str,
			  params: dict[str, any],
			  __async_session: "aiohttp.ClientSession") -> dict:
	"""
	params:
		group_id: str
		access_token=api_key: str
		v=version: str
	More info: https://dev.vk.com/ru/method/groups.getLongPollServer
	"""

	return __async_session.get(f'{url}/method/groups.getLongPollServer', params=params)


@utils.async_session_generator(handleResponseStatus)
def getSessionEvent(*,
			poll_session: dict[str, any],
			__async_session: "aiohttp.ClientSession") -> dict:
	server = poll_session['server']
	key = poll_session['key']
	ts = poll_session['ts']
	wait = poll_session.get('wait', 25) # not necessary

	"""
	Request to server given by getLongPollServer. Fetch new event
	More info: https://dev.vk.com/ru/api/bots-long-poll/getting-started
	"""

	return __async_session.get(f'{server}?act=a_check&key={key}&ts={ts}&wait={wait}')


async def vkStartPolling(*,
			 url: str,
			 group_id: str,
			 access_token: str,
			 v: str,
			 onUpdate: callable = None):

	if onUpdate is None:
		def handle(update):
			print(update)
		onUpdate = handle
	
	params = {
		"group_id": group_id,
		"access_token": access_token,
		"v": v,
	}
	session = (await getLongPollServer(
			url=url,
			params=params))['response']

	async for updates in getSessionEvent(poll_session=session):

		"""
		More about 'failed' handling:
		https://dev.vk.com/ru/api/bots-long-poll/getting-started
		(scroll down)
		"""
		failed = updates.get('failed', 0)

		if failed == 2:
			session = (await getLongPollServer(
				url=url,
				params=params))['response']
			session['ts'] = updates['ts']
			continue
		if failed == 3:
			session = (await getLongPollServer(
				url=url,
				params=params))['response']
			continue

		session['ts'] = updates['ts']

		for update in updates.get('updates', []):

			update_processing = onUpdate(update)
			if isinstance(update_processing, utils.CoroutineType):
				await update_processing


if __name__ == "__main__":

	from dotenv import load_dotenv
	import os
	import asyncio
	
	
	load_dotenv()
	
	API_KEY = os.getenv("VK_API")
	GROUP_ID = os.getenv("VK_GROUP")
	URL = os.getenv("VK_URL")
	VERSION = os.getenv("VK_VERSION")
	
	def handleUpdate(update):
		print(update)

	asyncio.run(vkStartPolling(
			url=URL,
			access_token=API_KEY,
			group_id=GROUP_ID,
			v=VERSION,
			onUpdate=handleUpdate,
	))
