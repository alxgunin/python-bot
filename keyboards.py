from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton

ask_button = KeyboardButton("/ask_weather")
return_button = KeyboardButton("/main")
loc_button = KeyboardButton("Отправить геолокацию", request_location=True)

main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(ask_button, return_button)
loc_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(loc_button, return_button)