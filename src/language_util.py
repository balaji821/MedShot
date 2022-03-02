from deep_translator import GoogleTranslator
from configparser import ConfigParser

config: ConfigParser
lang_code_map: dict
lang_list: list


def init(cfg):
    global config
    global lang_code_map
    global lang_list
    config = cfg
    lang_list = GoogleTranslator.get_supported_languages()
    lang_code_map = GoogleTranslator.get_supported_languages(as_dict=True)
    for lang in lang_list:
        lang_code_map[lang_code_map[lang]] = lang


def get_all_langs():
    return lang_list


def get_translator(trgt):
    return GoogleTranslator(source='en', target=trgt)


def get_lang_name(lang_code):
    return lang_code_map[lang_code]


def get_lang_code(lang_name):
    return lang_code_map[lang_name]


def get_translated_message(message, chat_id):
    lang = get_preferred_language(chat_id)
    if lang == 'en':
        return message
    return get_translator(lang).translate(message)


def get_preferred_language(chat_id):
    return config.get("LANGUAGE-OPTIONS", str(chat_id))
