import time

import telebot
from cub_bot.bot_utils.logger import logger
from django.core.management.base import BaseCommand
from loader import bot_token
from telebot import types

bot: telebot.TeleBot = telebot.TeleBot(bot_token)


@bot.message_handler(commands=["start"])
def start(message: types.Message, res=False):
    bot.send_message(message.chat.id,
                     '⬇Ничего не понимаю вот кнопка внизу она все поймет',)

@bot.message_handler(content_types=["text"])
def handle_text(message):
    bot.send_message(message.chat.id,
                     '⬇Ничего не понимаю вот кнопка внизу она все поймет')


class Command(BaseCommand):
    """ Команда для запуска бота """

    def handle(self, *args, **options):
        try:
            bot.remove_webhook()
            logger.error('Start polling')
            bot.infinity_polling()
        except Exception as e:
            logger.error(e)
            time.sleep(3)
