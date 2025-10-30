from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram import types


def generate_opting_keyboard(answers_options, right_answers):
    builder = InlineKeyboardBuilder()
    for option in answers_options:
        builder.add(types.InlineKeyboardButton(text=option,
                                               callback_data="right_answer" if option == right_answers else "wrong_answer"
                                               ))
    builder.adjust(1)
    return builder.as_markup()

def cmd_start_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Начать викторину", resize_keyboard=True))
    return builder.as_markup()

def final_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Посмотерть статистику", resize_keyboard=True), types.KeyboardButton(text='Сбросить результаты и начать заново quiz', resize_keyboard=True))
    return builder.as_markup()
