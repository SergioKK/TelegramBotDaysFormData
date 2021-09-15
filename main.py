import random
from datetime import *
import telebot
from telebot import types

import config
import time
import re

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=["start"])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton(f"/start")
    item2 = types.KeyboardButton(f"{random.randint(1000, 2021)}-{random.randint(10, 12)}-{random.randint(1, 30)}")

    markup.add(item1, item2)

    bot.send_message(
        message.chat.id,
        "Привет, {0.first_name}!\n"
        "Меня зовут - <b>{1.first_name}</b>.\n"
        "Я могу посчитать сколько прошло дней от любого момента из прошлого\n"
        "Введите дату в формате год-месяц-день".format(
            message.from_user, bot.get_me()
        ),
        parse_mode="html",
        reply_markup=markup,
    )


@bot.message_handler(content_types=["text"])
def conversation(message):
    if message.chat.type == "private":
        try:
            message_text = message.text.split()

            match = re.search(r"\d{4}-\d{2}-\d{2}", message_text[0])
            dt = time.strptime(match.group(), '%Y-%m-%d')

            today = date.today()
            incoming_data = date(dt.tm_year, dt.tm_mon, dt.tm_mday)
            result = today - incoming_data

            bot.send_message(message.chat.id, f'{str(result.days)} дней прошло с {message_text[0]}')

        except:
            bot.send_message(
                message.chat.id,
                f"Я вас не понимаю, попробуйте еще раз\n"
                f"Формат даты: год-месяц-день",
            )


# RUN
bot.polling(none_stop=True)
