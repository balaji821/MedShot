import googletrans
from configparser import ConfigParser
import requests
from urllib.parse import quote_plus as urlencode
import json

config: ConfigParser
url: str
headers: dict
payload: str
all_langs: dict


def init(cfg):
    global config
    global url
    global headers
    global payload
    global all_langs

    config = cfg
    url = "https://google-translate1.p.rapidapi.com/language/translate/v2"
    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'accept-encoding': "application/gzip",
        'x-rapidapi-host': "google-translate1.p.rapidapi.com",
        'x-rapidapi-key': "a5b77f7e45msh16b3b6f87f1e8f6p19671fjsn6d6556884bbf"
    }
    payload = "q={text}&target={trgt}&source={src}"

    with open("resources/language_codes.json", "r") as lang_file:
        all_langs = json.load(lang_file)


def get_all_langs():
    return all_langs


def get_translation(text, trgt):
    response = requests.request("POST", url, data=payload.format(text=urlencode(text), trgt=trgt, src='en'),
                                headers=headers).json()
    return response['data']['translations'][0]


def get_lang_name(lang_code):
    return googletrans.LANGUAGES[lang_code]


def get_translated_message(message, chat_id):
    lang = config.get("LANGUAGE-OPTIONS", str(chat_id))
    return get_translation(message, lang)['translatedText']


