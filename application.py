import telebot
import logging
import src.file_utils as fu
import src.keyboard_markups as km
import src.model_utils as model
import src.language_util as lang_util
from src.plant_utils import Plants
from src.disease_utils import Disease
from telebot.types import Message, CallbackQuery, ReplyKeyboardRemove
from gtts import gTTS
from urllib.parse import unquote_plus

logging.basicConfig(
    filename=fu.get_log_directory() + "out.log",
    level=logging.DEBUG,
    format='%(asctime)s|[%(module)s::%(funcName)s]|[%(levelname)s]: %(message)s',
    datefmt='[%Y-%m-%d]|[%H:%M:%S]',
)
logger = logging.getLogger("medshot")

TOKEN = "5281537388:AAEswK-zOewo59LQVY28jah4_varSgwvAUA"
application = telebot.TeleBot(token=TOKEN)

logger.info("Loading language resources...")
config = fu.load_language_resources()
logger.info("Initializing language utils...")
lang_util.init(config)
logger.info("Loading model...")
download_model = (config.get("MODEL-CONFIG", 'download') == 'true')
download_url = config.get("MODEL-CONFIG", 'url')
logger.info("Download model flag: " + str(download_model))
model.load_model(download_model, download_url)
plants_util = Plants.get_instance()
disease_util = Disease.get_instance()

set_lang_flag = False
medication_flag = False
plant_flag = False


@application.message_handler(commands=["start"])
def start(message: Message):
    logger.info("New user: " + str(message.chat.id))
    application.send_message(message.chat.id, "Welcome!!")
    change_lang(message)


@application.message_handler(commands=["menu"])
def menu(message):
    application.send_message(message.chat.id,
                             "`|          `☘*__" +
                             lang_util.get_translated_message("MENU", message.chat.id) +
                             "__*☘`          |`",
                             reply_markup=km.get_menu_markup(message.chat.id), parse_mode="MarkdownV2")


def get_lang_condition(message: Message):
    global set_lang_flag
    return set_lang_flag


def get_medication_flag(message: Message):
    global medication_flag
    return medication_flag


def get_plant_flag(message: Message):
    global plant_flag
    return plant_flag


def to_speech(text, chat_id, language='en'):
    output_path = fu.get_audio_path() + str(chat_id) + ".mp3"
    output = gTTS(text=text, lang=language, slow=False)
    output.save(output_path)
    return open(output_path, 'rb')


@application.message_handler(func=get_lang_condition)
def set_language(message: Message):
    if message.text not in lang_util.get_all_langs():
        application.send_message(message.chat.id, "Language not recognized! Please select one from the list.",
                                 reply_markup=km.get_language_selection_markup())
        return
    lang_code = lang_util.get_lang_code(message.text)
    config.set("LANGUAGE-OPTIONS", str(message.chat.id), lang_code)

    logger.info(str(message.chat.id) + " chosen language: " + lang_util.get_lang_name(lang_code))

    fu.update_language_resources(config)

    global set_lang_flag
    global medication_flag
    global plant_flag
    set_lang_flag = False
    medication_flag = False
    plant_flag = False

    application.send_message(message.chat.id,
                             lang_util.get_translated_message("Language set to " + lang_util.get_lang_name(lang_code),
                                                              message.chat.id),
                             reply_markup=ReplyKeyboardRemove(selective=False))
    menu(message)


@application.message_handler(func=get_medication_flag)
def get_medication(message: Message):
    disease = message.text
    if "/" not in disease or disease.split("/")[1] not in disease_util.disease_to_plant_map:
        application.send_message(message.chat.id,
                                 lang_util.get_translated_message(
                                     "Disease not recognized! Please select one from the list.",
                                     message.chat.id),
                                 reply_markup=km.get_disease_markup(message.chat.id))
        return
    disease = disease.split("/")[1]
    application.send_message(message.chat.id,
                             lang_util.get_translated_message(" Herbs that can cure " + disease,
                                                              message.chat.id),
                             reply_markup=km.get_medication_markup(disease, message.chat.id))

    global set_lang_flag
    global medication_flag
    global plant_flag
    set_lang_flag = False
    medication_flag = False
    plant_flag = False


@application.message_handler(func=get_plant_flag)
def plant_info(message: Message):
    plant_name = message.text
    print(plant_name)
    if '/' not in plant_name:
        application.send_message(id,
                                 lang_util.get_translated_message("Herb not found! Please select one from the list.",
                                                                  id),
                                 reply_markup=km.get_plant_list_markup(id))
        return
    plant_name = plant_name.split("/")[1]
    print(plant_name)
    plant_name = plants_util.get_plant_common_name(plant_name, lang_util.get_preferred_language(message.chat.id))
    send_plant_info(plant_name, message.chat.id, True)

    global set_lang_flag
    global medication_flag
    global plant_flag
    set_lang_flag = False
    medication_flag = False
    plant_flag = False


def send_plant_info(plant, id, send_plant_image):
    if plant not in plants_util.get_plant_list(lang_util.get_preferred_language(id)):
        application.send_message(id,
                                 lang_util.get_translated_message("Herb not found! Please select one from the list.",
                                                                  id),
                                 reply_markup=km.get_plant_list_markup(id))
        return
    logger.info(str(id) + " requested info on" + plant)
    application.send_message(id,
                             "`          `🍃*__" +
                             lang_util.get_translated_message(plant, id) +
                             "__*🍃`       ‎`", parse_mode="MarkdownV2")
    if not plant == 'None' and not send_plant_image:
        send_pant_image(id,
                        plants_util.get_plant_sci_name_with_common_name(plant, lang_util.get_preferred_language(id)))
    message_to_send = lang_util.get_translated_message(
        plants_util.get_info(plant, lang_util.get_preferred_language(id)),
        id)
    uses_heading = lang_util.get_translated_message("Uses", id)
    info_heading = "`          `👇🏻*__" + \
                   lang_util.get_translated_message("Information", id) + \
                   "__*👇🏻`       ‎`\n" + ("\\-\\-" * 21)

    application.send_message(id, info_heading, parse_mode="MarkdownV2")
    application.send_message(id, message_to_send)
    application.send_audio(id,
                           to_speech(message_to_send, id, language=lang_util.get_preferred_language(id)),
                           reply_markup=ReplyKeyboardRemove())
    application.send_message(id, "`          `__" + uses_heading +
                                 "__`       ‎`\n",
                             reply_markup=km.get_plant_info_markup(plant, id), parse_mode="MarkdownV2")


@application.callback_query_handler(func=lambda call: "use;" in call.data)
def plant_use_info(call: CallbackQuery):
    common_name = call.data.split(";")[1]
    use_case = call.data.split(";")[2]
    use_case = unquote_plus(use_case)
    message = plants_util.get_info(common_name, lang_util.get_preferred_language(call.message.chat.id), use_case)
    message = lang_util.get_translated_message(message, call.message.chat.id)
    use_heading = "__" + lang_util.get_translated_message(use_case, call.message.chat.id)\
        .replace("-", "\-").replace("_", " ") + "__"
    application.send_message(call.message.chat.id, use_heading, parse_mode="MarkdownV2")
    application.send_message(call.message.chat.id, message)
    application.send_audio(call.message.chat.id, to_speech(message, call.message.chat.id,
                                                           language=lang_util.get_preferred_language(
                                                               call.message.chat.id)))


@application.callback_query_handler(func=lambda call: call.data == "info")
@application.message_handler(commands=["info"])
def info_command(message: Message or CallbackQuery):
    if type(message) is CallbackQuery:
        message = message.message
    application.send_message(message.chat.id,
                             lang_util.get_translated_message("__Get information on a herb__", message.chat.id),
                             parse_mode="MarkdownV2")
    application.send_message(message.chat.id,
                             lang_util.get_translated_message("Select from the list of herbs given below",
                                                              message.chat.id),
                             reply_markup=km.get_plant_list_markup(message.chat.id))
    global plant_flag
    plant_flag = True


@application.callback_query_handler(func=lambda call: call.data == "medication")
@application.message_handler(commands=["medication"])
def get_medication(message: Message or CallbackQuery):
    if type(message) is CallbackQuery:
        message = message.message
    application.send_message(message.chat.id,
                             lang_util.get_translated_message("__Find medication for a disease__", message.chat.id),
                             parse_mode="MarkdownV2")
    application.send_message(message.chat.id, lang_util.get_translated_message("Choose the disease", message.chat.id),
                             reply_markup=km.get_disease_markup(message.chat.id))

    global medication_flag
    medication_flag = True


@application.message_handler(commands=["lang"])
@application.callback_query_handler(func=lambda call: "change_lang" in call.data)
def change_lang(message: Message or CallbackQuery):
    if type(message) is CallbackQuery:
        message = message.message
    application.send_message(message.chat.id,
                             lang_util.get_translated_message("__Change Language__", message.chat.id),
                             parse_mode="MarkdownV2")
    application.send_message(message.chat.id, "Please choose your preferred language.",
                             reply_markup=km.get_language_selection_markup())
    global set_lang_flag
    set_lang_flag = True


def send_pant_image(id, sci_name):
    application.send_photo(id, plants_util.get_plant_image(sci_name))


@application.callback_query_handler(func=lambda call: "predict" in call.data)
def predict(call: CallbackQuery):
    application.send_message(call.message.chat.id,
                             lang_util.get_translated_message("__Identify a herb__", call.message.chat.id),
                             parse_mode="MarkdownV2")
    application.send_message(call.message.chat.id,
                             lang_util.get_translated_message("Please send a photograph of the plant.",
                                                              call.message.chat.id))


@application.message_handler(content_types=["photo"])
def identify_plant(message: Message):
    download_loc = download_image(message)
    result = model.make_prediction(download_loc)
    logger.info("Prediction made by " + str(message.chat.id) + ": " + str(result))
    sci_name = plants_util.get_plant_sci_name(result[0])
    common_name = plants_util.get_plant_common_name(sci_name, lang_util.get_preferred_language(message.chat.id))
    if common_name != "None":
        application.send_message(message.chat.id, lang_util.get_translated_message(
            "Herb is identified as " + common_name + "(" + sci_name + ")", message.chat.id))
    send_plant_info(common_name, message.chat.id, False)


@application.message_handler(content_types=["document"])
def document_error(message: Message):
    application.send_message(message.chat.id, lang_util.get_translated_message(
        "Please send image as a photo (_Tip: Choose image from your gallery_)", message.chat.id),
                             parse_mode="MarkdownV2")


def download_image(message: Message):
    image_path = fu.get_test_images_dir() + str(message.chat.id) + ".jpg"
    logger.info("Downloading image: " + image_path)
    file = application.get_file(message.photo[-1].file_id)
    image_bytes = application.download_file(file.file_path)
    fu.save_image(image_bytes, image_path)
    logger.info("Download success: " + image_path)
    return image_path


print("Bot started.")
application.infinity_polling()
