import telebot
from telebot import types
from bs4 import BeautifulSoup
import requests

url = "https://www.olx.ua/uk/transport/legkovye-avtomobili/"
HEADERS = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}
token = ""
bot = telebot.TeleBot(token)
i_ = 0


def tele_bot():
    @bot.message_handler(commands=["start"])
    def send_message(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('Наступна')
        markup.add(item1)
        bot.send_message(message.chat.id, "Цей бот створений для пошуку автомобілів", reply_markup=markup)

    @bot.message_handler(content_types=['text'])
    def bot_message(message):
        global i_
        if message.chat.type == "private":
            if message.text == "Наступна":
                parser(message, i_)
                i_ += 1

    bot.polling()


def parser(message, index):
    req = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(req.text, "lxml")
    urls = soup.find_all("a", class_="thumb vtop inlblk rel tdnone linkWithHash scale4 detailsLink")
    if index < len(urls):
        items = urls[index]
        item_href = items.get("href")
        req_2 = requests.get(item_href, headers=HEADERS)
        soup_2 = BeautifulSoup(req_2.text, "lxml")
        car_info = soup_2.find("div", class_="css-1wws9er")
        car_Mark = car_info.find("h1", class_="css-1soizd2 er34gjf0").text
        car_Price = car_info.find("h3", class_="css-ddweki er34gjf0").text
        bot.send_message(message.chat.id, "[+] " + car_Mark + "\tЦіна: " + str(car_Price) + "\tСсилка: " + item_href)
    else:
        bot.send_message(message.chat.id, "Більше автомобілів немає.")


if __name__ == "__main__":
    tele_bot()
