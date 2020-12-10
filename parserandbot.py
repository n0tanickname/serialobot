import telebot
import sqlite3
from telebot import util
from sqlite3 import Error



def sql_read(title):
    database = sqlite3.connect('torrents.db3')

    num = []
    name = []
    hashes = []
    k = 0

    # title hash_info
    cursor = database.cursor()

    cursor.execute("SELECT title, hash_info FROM torrent")

    imp = cursor.fetchall()

    for clmn in imp:
        title2 = str(clmn[0]).lower()
        sovpad = title2.find(title)
        if sovpad != -1:
            name.append(clmn[0])
            hashes.append(clmn[1])
            if k <= 4:
                k += 1
                num.append(k)
            else:
                f = open("data.txt", "w")
                for i in range(0, k):
                    hashes[i] = 'magnet:?xt=urn:btih:' + hashes[i]
                    name[i] = str(num[i]) + '.) ' + name[i]

                for i in range(0, k):
                    f.write(name[i] + "\n" + hashes[i] + "\n")
                exit()


bot = telebot.TeleBot('') #здесь должен быть токен бота


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет. Хочешь посмотерть сериал, но не знаешь где его найти? Введи сначала /download и название фильма(сериала) , а после напиши /links')
@bot.message_handler(commands=['download'])
def handle_text(message):
    cid = message.chat.id
    msgName = bot.send_message(cid, 'Введи название:')
    bot.register_next_step_handler(msgName , step_Set_Name)
def step_Set_Name(message):
    cid = message.chat.id
    title = message.text
    sql_read(title)

@bot.message_handler(commands=['links'])
def function_name(message):
    file1 = open('data.txt', 'rb')
    bot.send_document(message.chat.id, file1)

bot.polling(none_stop=True, interval=0)
