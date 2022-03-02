from telebot import types
import language_util as langs

menu = {"Identify a plant": "predict", "Get information on a plant": "info"}


def get_menu_markup():
    markup = types.InlineKeyboardMarkup(row_width=1)
    for item in menu:
        markup.add(types.InlineKeyboardButton(item, callback_data=menu[item]))
    return markup


def get_language_selection_markup():
    keyboard = []
    row = []
    for lang_code, lang in langs.get_all_langs().items():
        if len(row) < 5:
            row.append(types.InlineKeyboardButton(lang, callback_data="set_lang_"+lang_code))
        else:
            keyboard.append(row)
            row = []
    markup = types.InlineKeyboardMarkup(keyboard=keyboard)
    return markup
