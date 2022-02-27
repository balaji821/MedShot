import googletrans
from googletrans import Translator
from configparser import ConfigParser

translator: Translator = Translator()
config: ConfigParser


def init(cfg):
    global config
    config = cfg


def get_translation(text, dest):
    return translator.translate(text, dest, 'en')


def get_lang_name(lang_code):
    return googletrans.LANGUAGES[lang_code]


def get_translated_message(message, chat_id):
    lang = config.get("LANGUAGE OPTIONS", str(chat_id))
    return get_translation(message, 'ta').text


# print(get_translated_message("Herb is identified as ", ""))
