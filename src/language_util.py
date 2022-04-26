from deep_translator import GoogleTranslator
from configparser import ConfigParser
from pandas import DataFrame

config: ConfigParser
lang_code_map: dict
lang_list: list
translation_cache: dict


def init(cfg):
    global config
    global lang_code_map
    global lang_list
    global translation_cache
    config = cfg
    lang_list = GoogleTranslator().get_supported_languages()
    lang_code_map = GoogleTranslator().get_supported_languages(as_dict=True)
    for lang in lang_list:
        lang_code_map[lang_code_map[lang]] = lang
    translation_cache = {}


def get_all_langs():
    return lang_list


def get_translator(trgt):
    return GoogleTranslator(source='en', target=trgt)


def get_lang_name(lang_code):
    return lang_code_map[lang_code]


def get_lang_code(lang_name):
    return lang_code_map[lang_name]


def translate(message, language):
    translator = get_translator(language)
    translated_message: str = ""
    if len(message) < 5000:
        translated_message = translator.translate(message)
    else:
        for i in range(len(message)//5000):
            batch = message[i*5000:(i+1)*5000]
            translated_message += translator.translate(batch)
    return translated_message


def get_translated_message(message, chat_id):
    lang = get_preferred_language(chat_id)
    if message in translation_cache:
        translation: dict = translation_cache[message]
        if lang in translation:
            return translation[lang]
        else:
            translation[lang] = translate(message, lang)
            return translation[lang]
    else:
        translation_cache[message] = {lang: translate(message, lang)}
        return translation_cache[message][lang]


def get_preferred_language(chat_id):
    return config.get("LANGUAGE-OPTIONS", str(chat_id))
