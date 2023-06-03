import telebot
from telebot import types
import cv2
import qrcode
from pyzbar.pyzbar import decode
from language import *
from translate import Translator

TOKEN = "6056361778:AAGeWjV4JXRj5zkEZbrCdRYhBbDS0gbZ6Y4"
bot = telebot.TeleBot(TOKEN)

create_table()

to_lang = "en"

@bot.message_handler(commands=["start"])
def send_welcome(message):
    global to_lang
    set_language_code(to_lang, message.from_user.username)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item = types.KeyboardButton("Change a language")
    markup.add(item)

    _text = f"""Hi, {message.chat.first_name}, 
i can code your text in QR-code To code information in QR-code."""
    bot.send_message(message.chat.id, translate(_text), reply_markup=markup)
    bot.message_handler(message.chat.id, translate("Input the text"))

text = ""
@bot.message_handler(content_types=["text"])
def code(message):
    global text, to_lang
    if message.text == translate("Code"):
        img = qrcode.make(text)
        img.save("image.png", "png")
        photo = open("image.png", "rb")
        bot.send_photo(message.chat.id, photo)
        photo.close()
    elif message.text == translate("Decode"):
        bot.send_message(message.chat.id, "Send a QR-code")
    elif message.text == "Change a language":
        markup = types.InlineKeyboardMarkup(row_width=2)
        item1 = types.InlineKeyboardButton("🇬🇧", callback_data="en")
        item2 = types.InlineKeyboardButton("🇺🇦", callback_data="uk")
        markup.add(item1, item2)
        bot.send_message(message.chat.id, "Choose a language/Виберіть мову", reply_markup=markup)
    else:
        text = str(message.text)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item = types.KeyboardButton(translate("Code"))
        item2 = types.KeyboardButton(translate("Decode"))
        markup.add(item, item2)
        print(f"{message.chat.first_name}: {message.text}")
        bot.send_message(message.chat.id, translate("To get a QR-code press a button"), reply_markup=markup)

@bot.message_handler(content_types=["photo"])
def _decode(message):
    try:
        file_id = message.photo[0].file_id
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        with open("downloaded_image.jpg", 'wb') as new_file:
            new_file.write(downloaded_file)

        img_qrcode = cv2.imread("downloaded_image.jpg")
        data = decode(img_qrcode)[0]

        bot.send_message(message.chat.id, translate(f"Data : ") + str(data.data.decode("utf-8")))
    except IndexError:
        bot.send_message(message.chat.id, translate("Unfortunately, finding the QR-code is unsuccessfully"))



@bot.callback_query_handler(func=lambda call: True)
def translate_message(call):
    global to_lang
    print(call.data)
    set_language(call.data, call.message.chat.username)
    to_lang = get_language(call.message.chat.username)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                          text=translate("You choosed a language"))

def translate(text):
    global to_lang
    translator = Translator(to_lang=to_lang)
    return translator.translate(text)

bot.infinity_polling()