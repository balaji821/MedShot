import telebot
import telebot.types as types
import logging
import file_utils as fu
import keyboard_markups as km
import model_utils as model
import language_util as lang_util
from plant_utils import Plants

logging.basicConfig(
    filename=fu.get_log_directory() + "out.log",
    level=logging.DEBUG,
    format='%(asctime)s|[%(module)s::%(funcName)s]|[%(levelname)s]: %(message)s',
    datefmt='[%Y-%m-%d]|[%H:%M:%S]',
)
logger = logging.getLogger("medshot")

TOKEN = "5281537388:AAEswK-zOewo59LQVY28jah4_varSgwvAUA"
bot = telebot.TeleBot(token=TOKEN)

config = fu.load_language_resources()
lang_util.init(config)
model.load_model()
plant_names = Plants()


# @bot.message_handler()
# def test(message):
#     bot.send_message(message.chat.id, message.text)


@bot.message_handler(commands=["start", "help"])
def start(message: types.Message):
    logger.info("New user: " + str(message.chat.id))
    bot.send_message(message.chat.id, "Please choose a language.", reply_markup=km.get_language_selection_markup())


@bot.callback_query_handler(func=lambda call: "predict" in call.data)
def predict(call: types.CallbackQuery):
    logger.info("Invoked predict method from keyboard markup.")
    bot.send_message(call.message.chat.id,
                     lang_util.get_translated_message("Please send a clear image of the plant.", call.message.chat.id))


@bot.message_handler(content_types=["photo"])
def identify_plant(message: types.Message):
    download_loc = download_image(message)
    result = model.make_prediction(download_loc)
    logger.info("Prediction made by "+str(message.chat.id)+": "+str(result))
    bot.send_message(message.chat.id, lang_util.get_translated_message(
        "Herb is identified as " + plant_names.get_plant_common_name(result[0]) + "(" + plant_names.get_plant_sci_name(
            result[0]) + ")", message.chat.id), reply_markup=km.get_menu_markup())


@bot.callback_query_handler(func=lambda call: "set_lang_" in call.data)
def set_language(call: types.CallbackQuery):
    lang_code = call.data[-2:]
    config.set("LANGUAGE-OPTIONS", str(call.message.chat.id), lang_code)

    logger.info(str(call.message.chat.id) + " chosen language: " + lang_util.get_lang_name(lang_code))

    fu.update_language_resources(config)
    bot.send_message(call.message.chat.id,
                     lang_util.get_translated_message("Language set to " + lang_util.get_lang_name(lang_code), call.message.chat.id),
                     reply_markup=km.get_menu_markup())


def download_image(message: types.Message):
    image_path = fu.get_images_dir() + str(message.chat.id) + ".jpg"
    logger.info("Downloading image: " + image_path)
    file = bot.get_file(message.photo[-1].file_id)
    image_bytes = bot.download_file(file.file_path)
    fu.save_image(image_bytes, image_path)
    logger.info("Download success: " + image_path)
    return image_path


print("Bot started.")
bot.infinity_polling()
