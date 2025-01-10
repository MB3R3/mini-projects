from dotenv import load_dotenv
from json import load
import os
import requests
import telebot

"""
This file shows a simple way to configure a telegram bot 
that returns a user's daily horoscope from your zodiac sign
with simple message handlers
"""

load_dotenv()
BOT_TOKEN = os.environ.get('BOT_TOKEN')

# print(BOT_TOKEN)

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Hello little Sucker")


# @bot.message_handler(func=lambda msg:True)
# def echo_all(message):
#     bot.reply_to(message, message.text)

def get_daily_horoscope(sign:str, day:str) -> dict:
    """Get daily horoscope for a zodiac sign.
    Keyword arguments:
    sign:str - Zodiac sign
    day:str - Date in format (YYYY-MM-DD) OR TODAY OR TOMORROW OR YESTERDAY
    Return:dict - JSON data
    """
    url = "https://horoscope-app-api.vercel.app/api/v1/get-horoscope/daily"
    params = {"sign":sign, "day":day}
    response = requests.get(url, params)

    return response.json()


@bot.message_handler(commands=['horoscope'])
def sign_handler(message):
    text = "What's your zodiac sign?\nChoose one: *Aries*, *Taurus*, *Gemini*, *Cancer,* *Leo*, *Virgo*, *Libra*, *Scorpio*, *Sagittarius*, *Capricorn*, *Aquarius*, and *Pisces*."
    sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(sent_msg, day_handler)


def day_handler(message):
    sign = message.text
    text = "What day do you want to know?\nChoose one: *TODAY*, *TOMORROW*, *YESTERDAY*, or a date in format YYYY-MM-DD."
    sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(sent_msg, fetch_horoscope, sign.capitalize())


def fetch_horoscope(message, sign):
    day = message.text
    horoscope = get_daily_horoscope(sign, day)
    data = horoscope["data"]
    # horoscope_message = f" *Horoscope:* {data['horoscope_data']}\\n*Sign:* {sign}\\*Day:* {data['date']}"
    horoscope_message = f'*Horoscope:* {data["horoscope_data"]}\\n*Sign:* {sign}\\n*Day:* {data["date"]}'
    bot.send_message(message.chat.id, "Here's your horoscope!")
    bot.send_message(message.chat.id, horoscope_message, parse_mode="Markdown")


bot.infinity_polling()


# def get_daily_horoscope(sign:str, day:str) -> dict:
#     """Get daily horoscope for a zodiac sign.
#     Keyword arguments:
#     sign:str - Zodiac sign
#     day:str - Date in format (YYYY-MM-DD) OR TODAY OR TOMORROW OR YESTERDAY
#     Return:dict - JSON data
#     """
#     url = "https://horoscope-app-api.vercel.app/api/v1/get-horoscope/daily"
#     params = {"sign":sign, "day":day}
#     response = requests.get(url, params)

#     return response.json()

# sign = "Aries"
# day = "TODAY"
# print(get_daily_horoscope(sign, day))