import telebot
import logging
import src.file_utils as fu
import src.keyboard_markups as km
import src.model_utils as model
import src.language_util as lang_util
from src.plant_utils import Plants
from telebot.types import Message, CallbackQuery, ReplyKeyboardRemove

logging.basicConfig(
    filename=fu.get_log_directory() + "out.log",
    level=logging.DEBUG,
    format='%(asctime)s|[%(module)s::%(funcName)s]|[%(levelname)s]: %(message)s',
    datefmt='[%Y-%m-%d]|[%H:%M:%S]',
)
logger = logging.getLogger("medshot")

TOKEN = "5281537388:AAEswK-zOewo59LQVY28jah4_varSgwvAUA"
application = telebot.TeleBot(token=TOKEN)
bot = application

logger.info("Loading language resources...")
config = fu.load_language_resources()
logger.info("Initializing language utils...")
lang_util.init(config)
logger.info("Loading model...")
download_model = (config.get("MODEL-CONFIG", 'download') == 'true')
download_url = config.get("MODEL-CONFIG", 'url')
logger.info("Download model flag: "+str(download_model))
model.load_model(download_model, download_url)
plants_util = Plants.get_instance()

set_lang_flag = False
plant_info_flag = False


@bot.message_handler(commands=["menu"])
def menu(message):
    bot.send_message(message.chat.id,
                     lang_util.get_translated_message("`|          `*__MENU__*`          |`", message.chat.id),
                     reply_markup=km.get_menu_markup(message.chat.id), parse_mode="MarkdownV2")


def set_lang_condition(message: Message):
    global set_lang_flag
    return set_lang_flag


@bot.message_handler(func=set_lang_condition)
def set_language(message: Message):
    if message.text not in lang_util.get_all_langs():
        bot.send_message(message.chat.id, "Language not recognized! Please select one from the list.",
                         reply_markup=km.get_language_selection_markup())
        return
    lang_code = lang_util.get_lang_code(message.text)
    config.set("LANGUAGE-OPTIONS", str(message.chat.id), lang_code)

    logger.info(str(message.chat.id) + " chosen language: " + lang_util.get_lang_name(lang_code))

    fu.update_language_resources(config)

    global set_lang_flag
    set_lang_flag = False

    bot.send_message(message.chat.id,
                     lang_util.get_translated_message("Language set to " + lang_util.get_lang_name(lang_code),
                                                      message.chat.id),
                     reply_markup=ReplyKeyboardRemove(selective=False))
    menu(message)


def send_plant_info(plant, id, send_plant_image):
    if plant not in plants_util.get_plant_list(lang_util.get_preferred_language(id)):
        bot.send_message(id,
                         lang_util.get_translated_message("Herb not recognized! Please select one from the list.", id),
                         reply_markup=km.get_plant_list_markup(id))
        return
    logger.info(str(id) + " requested info on" + plant)
    if not plant == 'None' and not send_plant_image:
        send_pant_image(id,
                        plants_util.get_plant_sci_name_with_common_name(plant, lang_util.get_preferred_language(id)))
    bot.send_message(id,
                     lang_util.get_translated_message(
                         plants_util.get_info(plant, lang_util.get_preferred_language(id)),
                         id),
                     reply_markup=km.get_plant_info_markup(plant, id))


@bot.callback_query_handler(func=lambda call: "info_" in call.data)
def plant_info(call: CallbackQuery):
    message: Message = call.message
    plant = call.data.split("_")[1]
    send_plant_info(plant, message.chat.id, True)
    menu(message)


@bot.callback_query_handler(func=lambda call: "use;" in call.data)
def plant_use_info(call: CallbackQuery):
    common_name = call.data.split(";")[1]
    use_case = call.data.split(";")[2]
    message = plants_util.get_info(common_name, lang_util.get_preferred_language(call.message.chat.id), use_case)
    message = lang_util.get_translated_message(message, call.message.chat.id)
    bot.send_message(call.message.chat.id, message)


@bot.message_handler(commands=["start"])
def start(message: Message):
    logger.info("New user: " + str(message.chat.id))
    bot.send_message(message.chat.id, "Welcome!!")
    change_lang(message)


@bot.callback_query_handler(func=lambda call: call.data == "info")
@bot.message_handler(commands=["info"])
def info_command(message: Message or CallbackQuery):
    if type(message) is CallbackQuery:
        message = message.message
    bot.send_message(message.chat.id, "Select from the list of available herbs",
                     reply_markup=km.get_plant_list_markup(message.chat.id))


@bot.message_handler(commands=["lang"])
@bot.callback_query_handler(func=lambda call: "change_lang" in call.data)
def change_lang(message: Message or CallbackQuery):
    if type(message) is CallbackQuery:
        message = message.message
    bot.send_message(message.chat.id, "Please choose your preferred language.",
                     reply_markup=km.get_language_selection_markup())
    global set_lang_flag
    set_lang_flag = True


def send_pant_image(id, sci_name):
    bot.send_photo(id, plants_util.get_plant_image(sci_name))


@bot.callback_query_handler(func=lambda call: "predict" in call.data)
def predict(call: CallbackQuery):
    bot.send_message(call.message.chat.id,
                     lang_util.get_translated_message("Please send a photograph of the plant.", call.message.chat.id))


@bot.message_handler(content_types=["photo"])
def identify_plant(message: Message):
    download_loc = download_image(message)
    result = model.make_prediction(download_loc)
    logger.info("Prediction made by " + str(message.chat.id) + ": " + str(result))
    sci_name = plants_util.get_plant_sci_name(result[0])
    common_name = plants_util.get_plant_common_name(sci_name, lang_util.get_preferred_language(message.chat.id))
    if common_name != "None":
        bot.send_message(message.chat.id, lang_util.get_translated_message(
            "Herb is identified as " + common_name + "(" + sci_name + ")", message.chat.id))
    send_plant_info(common_name, message.chat.id, False)


@bot.message_handler(content_types=["document"])
def document_error(message: Message):
    bot.send_message(message.chat.id, lang_util.get_translated_message(
        "Please send image as a photo (_Tip: Choose image from your gallery_)", message.chat.id),
                     parse_mode="MarkdownV2")
    menu(message)


def download_image(message: Message):
    image_path = fu.get_test_images_dir() + str(message.chat.id) + ".jpg"
    logger.info("Downloading image: " + image_path)
    file = bot.get_file(message.photo[-1].file_id)
    image_bytes = bot.download_file(file.file_path)
    fu.save_image(image_bytes, image_path)
    logger.info("Download success: " + image_path)
    return image_path


print("Bot started.")
application.infinity_polling()
