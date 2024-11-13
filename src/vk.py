import requests


def __responseSuccessful(response: requests.Response) -> bool:
	if response.status_code != 200:
		print("Failed to fetch data:", response.status_code)
		return False
	return True


def getLongPollServer(group_id: str, api_key: str, version: str = "5.199") -> dict:
	params = {
		"group_id": group_id,
		"access_token": api_key,
		"v": version
	}

	response = requests.get("https://api.vk.com/method/groups.getLongPollServer", params=params)

	if not __responseSuccessful(response):
		return {"Error": response.status_code}
	
	session_data = response.json()
	
	if "response" not in session_data:
		print("Error:", session_data.get("error", {}).get("error_msg", "Unknown error"))
		raise Exception("Failed to fetch data: no response field")
	
	return session_data["response"]

def getSessionEvent(server: str, key: str, ts: int, wait: int = 25) -> dict:

	response = requests.get(f'{server}?act=a_check&key={key}&ts={ts}&wait={wait}')
	
	if not __responseSuccessful(response):
		return {"Error": response.status_code}
	
	event_data = response.json()
	
	return event_data


if __name__ == "__main__":

	from dotenv import load_dotenv
	import os
	
	
	load_dotenv()
	
	API_KEY = os.getenv("VK_API")
	GROUP_ID = os.getenv("VK_GROUP")
	
	session = getLongPollServer(GROUP_ID, API_KEY)
	print(session)
	
	server = session["server"]
	key = session["key"]
	ts = session["ts"]
	
	event = getSessionEvent(server, key, ts, 5)
	print(event)
