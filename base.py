
import telebot
import requests
import json
import os
import time
import shadowfiendtop1mider as M249
from openai import OpenAI
from dotenv import load_dotenv
from telebot import types
from kinop_api import KP







load_dotenv()
client = OpenAI(api_key = os.getenv('API'))
kinopoisk = KP(os.getenv('KP'))
bot = telebot.TeleBot(os.getenv('TG'))




@bot.message_handler(commands=["start"])
def engine__up(message): 
    M249.add_id(message.from_user.id)
    bot.send_message(message.chat.id, "<b>Введите описание:</b>", parse_mode='html') 



@bot.message_handler(content_types=['text'])
def get_forgpt_answer(message):
    global list_anfilser
    response = client.chat.completions.create(
         model='gpt-4',
        messages=[{"role": "user", "content": f"Найди 10 фильмов/аниме/сериалов по описанию: {message.text} и выведи ТОЛЬКО их НАЗВАНИЯ в нумерации без лишнего текста"}],
        temperature=0.1,
        max_tokens=3000,
        frequency_penalty=0
    )
        
    anfilser = (response.choices[0].message.content)
    list_anfilser = anfilser.split('\n')
       
    markup = types.InlineKeyboardMarkup()
    dd = (types.InlineKeyboardButton(list_anfilser[0], callback_data=f"btn1|0"))
    markup.add(dd)
    dd1 = (types.InlineKeyboardButton(list_anfilser[1], callback_data=f"btn2|1"))
    markup.add(dd1)
    dd2 = (types.InlineKeyboardButton(list_anfilser[2], callback_data=f"btn3|2"))
    markup.add(dd2)
    dd3 = (types.InlineKeyboardButton(list_anfilser[3], callback_data=f"btn4|3"))
    markup.add(dd3)
    dd4 = (types.InlineKeyboardButton(list_anfilser[4], callback_data=f"btn5|4"))
    markup.add(dd4)
    dd5 = (types.InlineKeyboardButton(list_anfilser[5], callback_data=f"btn6|5"))
    markup.add(dd5)
    dd6 = (types.InlineKeyboardButton(list_anfilser[6], callback_data=f"btn7|6"))
    markup.add(dd6)
    dd7 = (types.InlineKeyboardButton(list_anfilser[7], callback_data=f"btn8|7"))
    markup.add(dd7)
    dd8 = (types.InlineKeyboardButton(list_anfilser[8], callback_data=f"btn9|8"))
    markup.add(dd8)
    dd9 = (types.InlineKeyboardButton(list_anfilser[9], callback_data=f"btn10|9"))
    markup.add(dd9)
    bot.send_message(message.chat.id, 'Результаты поиска🔎:', reply_markup=markup)
    
    


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    index = callback.data
    if index.startswith("btn"):
        pudge = list_anfilser[int(index.split("|")[1])][4:-1]
        search = kinopoisk.search(pudge)
  
       
        global list_buttons_txt
        list_buttons_txt = []
        list_buttons = []
        markup_panel = types.InlineKeyboardMarkup(row_width=1)
        i = -1
        for item in search:
            i+=1
            list_buttons_txt.append(item.ru_name)
            list_buttons.append(types.InlineKeyboardButton(item.ru_name, callback_data=f"fas|{i}"))    
        markup_panel.add(*list_buttons)
        
           
            
            
        
        
        bot.send_message(callback.message.chat.id, "Все похожие фильмы:", reply_markup=markup_panel)       
        
    elif index.startswith("fas"):
        pudge = list_buttons_txt[int(index.split("|")[1])]
        search = kinopoisk.search(pudge)
        for item in search:
            q = (item.year)
            qq = (", ".join(item.genres))
            qqq = (", ".join(item.countries))
            qqqq = (item.kp_rate)
            qqqqq = (item.kp_url)
            
            
            
        bot.send_message(callback.message.chat.id, f'''{pudge}:\
\n<b>Год выпуска:</b> {q},\
\n<b>Жанры:</b> {qq},\
\n<b>Страна производитель:</b> {qqq},\
\n<b>Рейтинг на Кинопоиске:</b> {qqqq}⭐\n
{qqqqq}''', parse_mode="html", disable_web_page_preview=False,) 
        
        
    else:
        bot.send_message(callback.message.chat.id, "Неизвестная ошибка!🚫")     
        
        
        
   
    
    
    
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)