import aiohttp.client
from aiogram.types import Location
import urllib

weather_api = "bc358ee9c85d2dfea47e9a830d40c24e"

kelvin0 = 273.15

def getDirection(angle):
	if angle <= 22.5 or angle >= (360 - 22.5):
		return "северный"
	elif angle > 22.5 and angle <= 67.5:
		return "северо-восточный"
	elif angle > 67.5 and angle <= 112.5:
		return "восточный"
	elif angle > 112.5 and angle <= 157.5:
		return "юго-восточный"
	elif angle > 157.5 and angle <= 202.5:
		return "южный"
	elif angle > 202.5 and angle <= 247.5:
		return "юго-западный"
	elif angle > 247.5 and angle <=292.5:
		return "западный"
	else:
		return "северо-западный"

def addEmoji(text):
	if "дождь" in text:
		return text + chr(127783)
	if "яcно" in text:
		return text + chr(127774)
	if "пасмурно" in text:
		return text + chr(9928)
	if "облачность" in text or "облачно" in text:
		return text + chr(127781)

class WeatherData:

	def __init__(self, temp, feels_like, description, place, speed, angle):
		description = addEmoji(description)
		self.temp = temp - kelvin0
		self.feels_like = feels_like - kelvin0
		if description:
			self.description = description.capitalize()
		else:
			self.description = ""
		self.place = place
		self.wind_speed = speed
		self.wind_direction = getDirection(angle)

class WeatherException(BaseException):
	pass

async def getCityWeather(city: str):
	return await makeRequest(getCityUrl(city))

async def getLocWeather(loc: Location):
	return await makeRequest(getLocUrl(loc))

def getCityUrl(city: str):
	return f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api}&lang=ru"

def getLocUrl(loc: Location):
	return f"http://api.openweathermap.org/data/2.5/weather?lat={loc.latitude}&lon={loc.longitude}&appid={weather_api}&lang=ru"

def parseResponse(json):
	return WeatherData(json["main"]["temp"], json["main"]["feels_like"], json["weather"][0]["description"], json["name"], json["wind"]["speed"], json["wind"]["deg"])

async def makeRequest(url: str):
	async with aiohttp.ClientSession() as session:
		async with session.get(url) as resp:
			if resp.status == 200:
				return parseResponse(await resp.json())

	raise WeatherException()