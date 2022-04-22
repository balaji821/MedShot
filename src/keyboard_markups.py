from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton, InlineKeyboardButton
import src.language_util as langs
from src.plant_utils import Plants
from src.disease_utils import Disease

menu = {"Identify a herb": "predict",
        "Find medication for a disease": "medication",
        "Get information on a herb": "info",
        "Change Language": "change_lang"}


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


def get_plant_list_markup(id):
    markup = InlineKeyboardMarkup(row_width=1)
    lang = langs.get_preferred_language(id)
    for plant in Plants.get_instance().get_plant_list(lang):
        if plant == "None":
            continue
        markup.add(InlineKeyboardButton(langs.get_translated_message(plant, id), callback_data="info_" + plant))
    return markup


def get_plant_info_markup(plant_name, id):
    plants = Plants.get_instance()
    lang = langs.get_preferred_language(id)
    sci_name = plants.get_plant_sci_name_with_common_name(plant_name, lang)
    uses: list[str] = list(plants.plant_info[sci_name]["uses"])
    uses.remove("info")

    markup = InlineKeyboardMarkup(row_width=2)

    i = 0
    while i < len(uses) - 1:
        markup.add(InlineKeyboardButton(langs.get_translated_message(uses[i].replace("_", " "), id),
                                        callback_data="use;" + plant_name + ";" + uses[i]),
                   InlineKeyboardButton(langs.get_translated_message(uses[i + 1].replace("_", " "), id),
                                        callback_data="use;" + plant_name + ";" + uses[i + 1])
                   )
        i += 2
    return markup


def get_disease_markup(id):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    lang = langs.get_preferred_language(id)
    for disease in Disease.get_instance().disease_to_plant_map:
        if lang == "en":
            markup.add(KeyboardButton(langs.get_translated_message(disease, id)))
        else:
            markup.add(KeyboardButton(langs.get_translated_message(disease, id) + "/" + disease))
    return markup


def get_medication_markup(disease: str, id):
    markup = InlineKeyboardMarkup(row_width=1)
    lang = langs.get_preferred_language(id)
    plant_list = Disease.get_instance().disease_to_plant_map[disease]

    for plant in plant_list:
        common_name = Plants.get_instance().get_plant_common_name(plant, lang)
        markup.add(InlineKeyboardButton(langs.get_translated_message(common_name, id),
                                        callback_data="use;" + common_name + ";" + disease))
    return markup
