import telebot

TOKEN = "5281537388:AAEswK-zOewo59LQVY28jah4_varSgwvAUA"
bot = telebot.TeleBot(token=TOKEN)


@bot.message_handler()
def test(message):
    bot.send_message(message.chat.id, message.text)


bot.polling()
