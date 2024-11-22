import utils


def handleResponseStatus(status):
	if status != 200:
		raise Exception(f'Error: {status}')


@utils.async_session_generator(handleResponseStatus)
def getUpdates(*, 
	       url: str,
	       params: dict[str, any],
		__async_session: "aiohttp.ClientSession"):
	"""
	params:
		offset: int
		limit: int
		timeout: int
		allowed_updates: list[int]
		
	More info: https://core.telegram.org/bots/api#getting-updates
	"""
	
	return __async_session.get(f'{url}/getUpdates', params=params)


@utils.async_session(handleResponseStatus)
def sendMessage(*,
		url: str,
		body: dict[str, any],
		__async_session: "aiohttp.ClientSession"):
	"""
	More info: https://core.telegram.org/bots/api#sendmessage
	"""

	return __async_session.post(f'{url}/sendMessage', data=body)


async def sendMessageInChat(*,
			    url: str,
			    api_key: str,
			    chat_id: int | str,
			    text: str,
			    **kwargs):
	body = {
		"chat_id": chat_id,
		"text": text,
	}
	for key, val in kwargs.items():
		body[key] = val
	
	return await sendMessage(
			url=f'{url}/bot{api_key}',
			body=body)


async def telegramStartPolling(*,
			       url: str,
			       api_key: str,
			       onUpdate: callable = None,
			       offset: int = 0,
			       timeout: int = 25,
			       **kwargs):
	if onUpdate is None:
		def handle(update):
			print(update)
		onUpdate = handle
	params = {
		'offset': offset,
		'timeout': timeout
	}
	for key, val in kwargs.items():
		params[key] = val

	# main cycle
	async for updates in getUpdates(
			url=f'{url}/bot{api_key}',
			params=params):

		for update in updates.get('result', []):
			params['offset'] = update['update_id'] + 1

			update_processing = onUpdate(update)
			if isinstance(update_processing, utils.CoroutineType):
				await update_processing


if __name__ == "__main__":
	import os
	from dotenv import load_dotenv
	import asyncio
	
	load_dotenv()
	
	API_KEY = os.getenv("TG_API")
	URL = os.getenv("TG_URL")
	def handleUpdate(update):
		print(update)

	async def run():
		await startPolling(
			api_key=API_KEY,
			onUpdate=handleUpdate)
	asyncio.run(run())
