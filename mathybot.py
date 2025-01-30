import os
from telebot import TeleBot, types

from constants import HELP_MESSAGE_FOR_QUDRATIC_EDUATION, HELP_MESSAGE_FOR_DIFF
from dotenv import load_dotenv
from mathy_logic import (delitel, discriminant, converter, roots,
                         differentiation)

load_dotenv()

bot = TeleBot(token=os.getenv('TOKEN'))


def keyboard_menu():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("/start")
    btn2 = types.KeyboardButton("/quadratic_eduation")
    btn3 = types.KeyboardButton("/diff")
    return keyboard.add(btn1, btn2, btn3)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'help_quadric':
                bot.send_message(
                    call.message.chat.id, HELP_MESSAGE_FOR_QUDRATIC_EDUATION
                )
            elif call.data == 'help_diff':
                bot.send_message(
                    call.message.chat.id, HELP_MESSAGE_FOR_DIFF
                )
    except Exception:
        bot.send_message(call.message.chat.id, 'Ошибка!')


@bot.message_handler(commands=['start'])
def start_command(message):
    menu = keyboard_menu()
    bot.send_message(
        message.chat.id, f'Hello {message.chat.username}', reply_markup=menu
    )


@bot.message_handler(commands=['quadratic_eduation'])
def quadratic_eduation_command(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('help', callback_data='help_quadric')
    markup.add(btn1)
    send_message = bot.send_message(
        message.chat.id,
        'Введите квадратое уравнение:',
        reply_markup=markup
    )
    bot.register_next_step_handler(send_message, quadratic_eduation)


def quadratic_eduation(message):
    chat_id = message.chat.id
    eduation = message.text
    message_text = ''
    try:
        message_text += f'Исходное уравнение: {eduation}\n'

        koef = delitel(eduation)
        if koef['a'] == 0:
            root = converter(-koef['c'] / koef['b']),

            message_text += 'Это не квадратное уравнение!\n'
        else:
            d = discriminant(koef['a'], koef['b'], koef['c'])
            root = roots(d, koef['a'], koef['b'])

            message_text += 'Коэффициенты:\na:{}\nb:{}\nc:{}\n'.format(
                koef['a'], koef['b'], koef['c']
            )
        if root:
            if len(root) == 1:
                message_text += 'Корень уравнения: {}\n'.format(*root)
            else:
                message_text += 'Корни уравнения: {}; {}\n'.format(*root)
        else:
            message_text += 'Корней нет!\n'

        bot.send_message(chat_id, message_text)
    except Exception as e:
        bot.send_message(
            chat_id,
            f'{e}\n{HELP_MESSAGE_FOR_QUDRATIC_EDUATION}'
        )


@bot.message_handler(commands=['diff'])
def diff_comand(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('help', callback_data='help_diff')
    markup.add(btn1)
    send_message = bot.send_message(
        message.chat.id,
        'Введите выражение:',
        reply_markup=markup
    )
    bot.register_next_step_handler(send_message, diff_eduation)


def diff_eduation(message):
    eduation = message.text
    message_text = ''

    try:
        message_text += f'Исходное выражение: {eduation}\n'

        diff = differentiation(eduation)

        message_text += f'{diff}'

        bot.send_message(message.chat.id, message_text)
    except Exception as e:
        bot.send_message(
            message.chat.id,
            f'{e}\n{HELP_MESSAGE_FOR_DIFF}'
        )


@bot.message_handler(content_types=['text'])
def say_hi(message):
    menu = keyboard_menu()

    chat = message.chat
    chat_id = chat.id

    bot.send_message(chat_id, 'Hello', reply_markup=menu)


bot.polling()
