from telebot import types
import googletrans

menu = {"Identify a plant":"predict", "Get information on a plant":"info"}


def get_menu_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for item in menu:
        markup.add(types.InlineKeyboardButton(item, callback_data=menu[item]))
    return markup


def get_language_selection_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
    for lang_code, lang in googletrans.LANGUAGES.items():
        markup.add(types.InlineKeyboardButton(lang, callback_data="set_lang_"+lang_code))
    return markup
