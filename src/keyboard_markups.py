from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton, InlineKeyboardButton
import language_util as langs

menu = {"Identify a herb": "predict", "Get information on a herb": "info", "Change Language": "change_lang"}


def get_menu_markup(chat_id):
    markup = InlineKeyboardMarkup(row_width=1)
    for item in menu:
        markup.add(InlineKeyboardButton(langs.get_translated_message(item, chat_id), callback_data=menu[item]))
    return markup


def get_language_selection_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    for lang in langs.get_all_langs():
        markup.add(KeyboardButton(lang))
    return markup
