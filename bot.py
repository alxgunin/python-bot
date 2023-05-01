import time
# import logging
from weather import *
from keyboards import *
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove
from datetime import datetime

api_token = '6175498507:AAFXPi7slq-buPQ0vjlExHBncOuLtMWwsrE'
bot = Bot(token=api_token)
dp = Dispatcher(bot=bot)
mode = "default"

def weatherMessage(weather):
	return f"{weather.place}, погода на {datetime.now().strftime('%Y-%m-%d, %H:%M')}:\n{weather.description}\nТемпература: {weather.temp:.1f}°C\nОщущается как: {weather.feels_like:.1f}°C\nВетер {weather.wind_direction}, {weather.wind_speed:.1f} м/с" 

@dp.message_handler(commands=['start', 'main'])
async def start_handler(message: types.Message):
	global mode
	mode = "default";
	user_id = message.from_user.id
	name = message.from_user.first_name
	await message.answer(f"Привет, {name}!\nЭтот бот может рассказать о погоде🌤\nИспользуйте /help, чтобы узнать о всех возможностях", reply_markup=main_keyboard)

@dp.message_handler(commands=['help'])
async def help_handler(message: types.Message):
	global mode
	mode = "default"
	user_id = message.from_user.id
	await message.answer("Вот, что я умею:\n/ask_weather - узнать погоду\n/main - вернуться в основное меню", reply_markup=main_keyboard)

@dp.message_handler(commands=["ask_weather"])
async def ask_handler(message: types.Message):
	global mode
	mode = "request"
	await message.answer("Введите город или отправьте геолокацию", reply_markup=loc_keyboard)

@dp.message_handler(content_types=["text"])
async def getWeather(message: types.Message):
	global mode
	if mode == "request":
		try:
			weather = await getCityWeather(message.text)
		except WeatherException:
			await message.reply("Не получилось найти город, попробуйте еще раз")
			return
		
		await message.answer(weatherMessage(weather))
	else:
		await message.reply("Я вас не понимаю, для помощи используйте /help")


@dp.message_handler(content_types=["location"])
async def getWeather(message: types.Message):
	try:
		weather = await getLocWeather(message.location)
	except WeatherException:
		await message.reply("Не получилось найти город, попробуйте еще раз")
		return

	await message.answer(weatherMessage(weather))

executor.start_polling(dp)