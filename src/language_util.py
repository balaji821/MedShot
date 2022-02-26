import googletrans
from googletrans import Translator

translator = Translator()
config = None

def init(cfg):
    global config
    config = cfg


def get_translation(text, dest):
    return translator.translate(text, dest)


def get_lang_name(lang_code):
    return googletrans.LANGUAGES[lang_code]


def get_translated_message(message, chat_id):
    lang = config.get(chat_id)
    return get_translation(message, lang)
