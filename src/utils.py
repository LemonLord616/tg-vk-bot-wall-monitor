from aiohttp import ClientSession


# from 'inspect' library
# https://github.com/python/cpython/blob/3.13/Lib/types.py
# line 30
async def _c(): pass
_c = _c()
CoroutineType = type(_c)
_c.close()


def async_session_generator(handleResponseStatus: callable = None):

	if handleResponseStatus is None:
		def handle(status):
			if status != 200:
				raise Exception(f'Error: {status}')
		handleResponseStatus = handle
	
	def error_handled_decorator(func: callable):
		"""
		Creates aiohttp session and generator in it
		"""
	
		async def wrapper(*args, **kwargs):
			async with ClientSession() as session:
				while True: #TODO: Some dependence (i.e. session_alive or whatever)
					response = await func(*args, **kwargs, __async_session=session)

					handleResponseStatus(response.status)
	
					yield await response.json()
		
		return wrapper
	return error_handled_decorator


def async_session(handleResponseStatus: callable = None):

	if handleResponseStatus is None:
		def handle(status):
			if status != 200:
				raise Exception(f'Error: {status}')
		handleResponseStatus = handle
	
	def error_handled_decorator(func):
		"""
		Async request
		"""
	
		async def wrapper(*args, **kwargs):
			async with ClientSession() as session:
				response = await func(*args, **kwargs, __async_session=session)

				handleResponseStatus(response.status)
	
				return await response.json()
		
		return wrapper
	return error_handled_decorator
