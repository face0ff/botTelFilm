#!/usr/bin/python
import requests
import urllib.request
from bs4 import BeautifulSoup
import config
import telebot
from telebot import types


headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
}

bot = telebot.TeleBot('1058544520:AAGVC0E4ify4mcse3X6MNEwtpRMiNkconCw')

markup_menu =types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=2)
btn_start = types.KeyboardButton("/start")
btn_address = types.KeyboardButton("Привет джули")

markup_menu.add(btn_start, btn_address)


@bot.message_handler(commands=['start'])
def handle_text(message):
    bot.send_message(message.chat.id, "Введите поиск", reply_markup = markup_menu)

    @bot.message_handler(content_types=['text'])
    def handle_text(message):
        global txt
        txt = message.text
        print(txt)

        payload = {"do": "search", "subaction": "search", "story": txt, "x": "32", "y": "13"}
        payload['story'] = txt
        # print(payload['story'])


        r = requests.post('http://ex-fs.net', data=payload, headers=headers)
        r.encoding = 'utf8'
        soup = BeautifulSoup(r.text, 'html.parser')

        sub_heading = soup.find(class_='SeaRchresultPostTitle')

        if sub_heading  == None:
            bot.send_message(message.chat.id, 'Soryan net takogo')
            
        else:
            link = sub_heading.find('a', href=True)
        
            linkTo = link['href']
            print(linkTo)
            

        

        txt1 = urllib.request.quote(txt.encode("utf8"))
        
        b = requests.get('http://www.ww.new-rutor.org/search/0/0/000/0', params=txt1, headers=headers)
        b.encoding = 'utf8'
        soup = BeautifulSoup(b.text, 'html.parser')
        b = b.url.replace('?', '')
                # bot.send_message(message.chat.id, b)
                # print (soup.prettify())

        d = requests.get(b, headers=headers)
        d.encoding = 'utf8'
        soup = BeautifulSoup(d.text, 'html.parser')
        print(soup.prettify())
        torrentL = soup.findAll('a', class_='downgif', limit=5)
        torrentn = soup.findAll('a', 'div', text= True)
        razmerT = soup.findAll('td', align="right", limit =10)

        for a in torrentn:
            for text in a.find_next_siblings(text=True):
            
                print (text.strip())

        spis= []

        spis2 = filter(lambda name: name.strip(), spis)

        for tot in razmerT:

            gb = tot.getText()

            spis.append(gb)

        print(torrentn)
        print(spis)
        print(*spis2)

        markup = types.InlineKeyboardMarkup()
        btn_my_site = types.InlineKeyboardButton('Описание', callback_data='info')
        #btn_my_razm = types.InlineKeyboardButton('Размер', callback_data='razm')
        btn_my_torrent = types.InlineKeyboardButton('Раздача на Руторе', callback_data='torrent')
        markup.add(btn_my_site, btn_my_torrent )
        bot.send_message(message.chat.id, 'Размер по порядку',  reply_markup=markup)

        bot.send_message(message.chat.id, '|'.join(spis))
        for i in torrentL:
            print(i)
            i.encoding = 'utf8'
            
            bot.send_message(message.chat.id, 'http://www.ww.new-rutor.org' + i['href'])

            @bot.callback_query_handler(func=lambda call:True)
            def call_back_info(call):
                if call.data == 'info':
                    bot.send_message(call.message.chat.id, linkTo )
           
                elif call.data == 'torrent':
                    bot.send_message(call.message.chat.id, b )


bot.polling(none_stop=True)
while True: 
    time.sleep(300)
