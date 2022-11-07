
import telebot
from telebot import types
import datetime
from requests import get
from bs4 import BeautifulSoup
bot = telebot.TeleBot('5605932312:AAFnYhy67qxt51hW4Q6moxWQFIRb0zHsMDM')
date_parse = datetime.date.today().strftime('%Y/%m/%d/')
@bot.message_handler(commands=['start']) #отслеживаем (обрабатываем) команду
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    news_button = types.KeyboardButton('Получить новости на сегодня')
    markup.add(news_button)
    mess = f'Привет, <b>{message.from_user.first_name}{message.from_user.last_name}</b>, я бот, который собирает новости. Я могу прислать тебе новости на сегодня в виде текстового файла.'
    bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=markup) #Отправка сообщения с картинкой в ответ на команду от пользователя
    photo = open('left-menu-news.png', 'rb')
    bot.send_photo(message.chat.id, photo)
#парсинг
url = 'https://www.mk.ru/news/' + date_parse
def parser(url):
    inf = BeautifulSoup(get(url).text, "html.parser")  # Отправляем запрос и варим суп
    news_list_html = inf.findAll('a', {'class': 'news-listing__item-link'})  # Извлекаем срез страницы с новостям
    news = []
    for n in news_list_html:  # Запускаем цикл перебора срезов
        news.append(n.find('h3').text.strip())  # Извлекаем текст новости
    return news
list_of_news = parser(url) #создание списка новостей
#Создание или переписывание файла с новостями
MyFile = open('news.txt', 'w', encoding='UTF-8')
#запись каждой новости в файл с помощью цикла
for element in list_of_news:
    MyFile.write(element)
    MyFile.write('\n\n')
MyFile.close()

@bot.message_handler(content_types=['text'])
def news(message):
    doc_file = open('news.txt', 'rb')
    if message.text == 'Получить новости на сегодня':
        bot.send_document(message.chat.id, doc_file) #отправка файла с новостями

bot.polling(none_stop=True)


