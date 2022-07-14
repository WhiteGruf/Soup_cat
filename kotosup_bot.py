from email import message
from http.client import BAD_REQUEST
import telebot
from telebot import types
from kotosup_menu import Food


bot = telebot.TeleBot("5418077308:AAEYDnH0flac9pG5-BmyBtzDhDXyayb1ARE")
sections = ["Завтраки","Каши","Супы","Сандвичи","Десерты","Горячие напитки","Холодные напитки","Слабоалкогольные напитки"]
section = ""
panckake_stuff = ["с ветчиной и сыром","с сулугуни и зеленью","с творогом и сметаной"]
menu = {}
dopping = []
menu_choice = ""
food_choice = ""
order = ""
user_name = ""
msg_id = 0
tea = Food("Чай").get_sections()
tea_name = tuple([i[0] for i in tea])
print(tea_name)

for i in sections:
    try:
        lst=[]
        for j in Food(i).get_sections():
            lst.append(j[0])
        menu[i]=lst
    except:
        pass
for i in Food("Доппинги").get_sections():
    dopping.append(i[0])
 

def start_one(message,txt):
    global msg_id
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1=types.InlineKeyboardButton(text="Меню", callback_data="Меню")
    item2=types.InlineKeyboardButton(text="О нас",callback_data="О нас")
    item3=types.InlineKeyboardButton(text="Что нового?", callback_data="Что нового")
    item4=types.InlineKeyboardButton(text="Заказ", callback_data="Заказ")
    markup.add(item1,item2,item3,item4)
    try:
        bot.edit_message_text(chat_id=message.chat.id,message_id=message.message_id,text= txt, reply_markup=markup)
       
    except Exception as e:
        #A request to the Telegram API was unsuccessful. Error code: 400. Description: Bad Request: message can't be edited
        if  msg_id and "400" in e.args[0] :
            print(e)
            bot.edit_message_text(chat_id=message.chat.id,message_id=msg_id,text= txt, reply_markup=markup)
        else:
            bot.send_message(message.chat.id,txt.format(message.from_user),reply_markup=markup)
        
def get_menu_one(message, txt):
    global order
 
    
    markup=types.InlineKeyboardMarkup(row_width=2)
    sections_btn=[]
    back_btn = types.InlineKeyboardButton(text="Назад", callback_data="Назад")
    for i in sections:
        sections_btn.append(
            types.InlineKeyboardButton(text=i,callback_data=i)
        )
    markup.add(*sections_btn,back_btn)
    bot.edit_message_text(chat_id=message.chat.id,message_id=message.message_id,text= txt, reply_markup=markup)

def comment_one(message, txt):

    markup=types.InlineKeyboardMarkup(row_width=2)
    order_chek = types.InlineKeyboardButton(text="Подтвердить заказ",callback_data="order_chek")
    clear = types.InlineKeyboardButton(text="Очистить заказ", callback_data="clear")
    comment = types.InlineKeyboardButton(text="Добавить комментарий", callback_data="add_comment")
    back_btn = types.InlineKeyboardButton(text="Назад", callback_data="Назад")
    markup.add(order_chek,clear,comment,back_btn)
    bot.edit_message_text(chat_id=message.chat.id,message_id=message.message_id,text= txt,reply_markup=markup)
    #bot.register_next_step_handler(message,get_comment)


@bot.message_handler(commands=["start"])
def start(message):
    global user_name
    user_name = message.from_user.first_name
    text = 'Привет, {0.first_name}. Я цифровой котик из кафе "Суп с котом". Скажи, с чего мы начнём?'
  
    start_one(message, text)

@bot.callback_query_handler(func=lambda callback: True)
def answer_callback(callback):
    global menu_choice
    global food_choice
    global order
    global user_name
    global tea
    global tea_name
    global msg_id
 
    if callback.data == "Что нового":
        markup=types.InlineKeyboardMarkup(row_width=2)
        url_btn = types.InlineKeyboardButton(text="Наш чат",url="https://t.me/kotosup")
        back_btn = types.InlineKeyboardButton(text="Назад", callback_data="Назад")
        markup.add(url_btn,back_btn)
        bot.edit_message_text(chat_id=callback.message.chat.id,message_id=callback.message.message_id,text= "Рад, что ты спросил. Тут мы публикуем все новости, заглядывай.", reply_markup=markup)
    # ИНФОРМАЦИЯ О КАФЕ
    elif callback.data == "О нас":

        markup=types.InlineKeyboardMarkup(row_width=2)
        back_btn = types.InlineKeyboardButton(text="Назад", callback_data="back_geo")
        markup.add(back_btn)

        bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,text= 
            '''Мы - кафе "Суп с котом". У нас много места, сытные и вкусные блюда и разные супы каждый день. 
        Также в кафе есть крутое арт-простанство, в котором регулярно проводятся интересные мероприятия. 
        Если ты творческий человек и хочешь устроить что-то свое, то всегда можешь связаться с нами и обсудить.''', 
            reply_markup=markup
        )
        #кнопка-ссылка на ко-ото из руководства
        bot.send_location(callback.message.chat.id, 54.186865, 37.609820)
    # МЕНЮ
    elif callback.data == "Меню" or callback.data == 'back_to_menu':
        get_menu_one(callback.message, "Вот разделы меню. Выбирай, что нужно, а я подробнее обо всём расскажу ;)")    
   
    elif callback.data == "Заказ":
        if order != "":
            comment_one(callback.message, order.replace("dopping", "Добавка: "))
            #bot.edit_message_text(chat_id=callback.message.chat.id,message_id=callback.message.message_id,text= order.replace("dopping", "Добавка: "), reply_markup=markup)
        else:
            comment_one(callback.message, "Пусто")
            #bot.edit_message_text(chat_id=callback.message.chat.id,message_id=callback.message.message_id,text= "Пусто", reply_markup=markup)
    elif callback.data == "order_chek":
            order = order.replace("dopping", "Добавка: ")
            bot.send_message("5219042303",user_name + "\n"+order)
            order = ""
            get_menu_one(callback.message, "Уже готовится")
    elif callback.data == "clear":
        order = ""
        start_one(callback.message, "Ваш заказ обнулён")
    elif callback.data == "add_comment":
        msg_id = callback.message.message_id
        #bot.edit_message_text(chat_id=callback.message.chat.id,message_id=callback.message.message_id,text= "Просто напишите комментарий",reply_markup=markup)
        comment_one(callback.message, "Напишите ва шкомментарий")
        bot.register_next_step_handler(callback.message,get_comment)
    
    # ОБРАБОТКА КНОПКИ "НАЗАД"
    elif callback.data == 'Назад':
        start_one(callback.message,'Привет, {0.first_name}. Я цифровой котик из кафе "Суп с котом". Скажи, с чего мы начнём?' )
    # ОБРАБОТКА КНОПКИ "НАЗАД" из сообщения с геопозицией
    elif callback.data =="back_geo":
        bot.delete_message(callback.message.chat.id,message_id=callback.message.message_id)
        start_one(callback.message,'Привет, {0.first_name}. Я цифровой котик из кафе "Суп с котом". Скажи, с чего мы начнём?' )
    
    elif callback.data == "Чай":
        markup = types.InlineKeyboardMarkup(row_width=1)
        tea_btn = []
        menu_choice = callback.data
        for i in tea:
            tea_btn.append(types.InlineKeyboardButton(text=i[0], callback_data=i[0]))#SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS
        back_btn = types.InlineKeyboardButton(text="Назад", callback_data="back_to_menu")
        markup.add(*tea_btn, back_btn)
        bot.edit_message_text(chat_id=callback.message.chat.id,message_id=callback.message.message_id,text= "Выберите чай",reply_markup=markup)
    # ОТОБРАЖЕНИЕ ЕДЫ

    # ИНФОРМАЦИЯ ПО АЛКОГОЛЮ
    elif callback.data=="Слабоалкогольные напитки":
            markup=types.InlineKeyboardMarkup(row_width=2)
            back_btn = types.InlineKeyboardButton(text="Назад", callback_data="back_to_menu")
            markup.add(back_btn)

            bot.edit_message_text(
                chat_id=callback.message.chat.id,
                message_id=callback.message.message_id,text= 
                '''Мы предлагаем несколько сортов пива и сидра от тульских производителей на любой вкус. Подробности можно узнать у барной стойки.''', 
                reply_markup=markup
            )
    # ОТОБРАЖЕНИЕ ЕДЫ ИЗ ВЫБРАННОГО РАЗДЕЛА
    elif callback.data in sections:
            
            menu_choice = callback.data
            markup=types.InlineKeyboardMarkup(row_width=2)
            food_btn=[]
            back_btn = types.InlineKeyboardButton(text="Назад", callback_data="back_to_menu")
            for i in menu[callback.data]:
                food_btn.append(
                    types.InlineKeyboardButton(text=i,callback_data=i)
                )
            markup.add(*food_btn,back_btn)
            bot.edit_message_text(chat_id=callback.message.chat.id,message_id=callback.message.message_id,text= 'Отличный выбор, вот все блюда из раздела:', reply_markup=markup)
    # ИНФОРМАЦИЯ О БЛЮДЕ И ВОЗМОЖНОСТЬ ЗАКАЗА
    elif callback.data in menu.get(menu_choice,tea_name) :    
        food_choice = callback.data
        

        if ("Сандвич" in food_choice and not "арахис" in food_choice) or menu_choice == "Горячие напитки" or menu_choice=="Чай":
            order_data = "choice_size"
        else:
            order_data = "ordering"

        markup=types.InlineKeyboardMarkup(row_width=1)
        back_btn = types.InlineKeyboardButton(text="Назад", callback_data="back_to_menu")
        order_btn = types.InlineKeyboardButton(text="Добавить в заказ", callback_data=order_data)
        markup.add(order_btn,back_btn)
        try:
            bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,text= 
            "\n".join(Food(menu_choice).get_food(callback.data)), 
            reply_markup=markup
            )
        except:
            get_menu_one(callback.message, "что-то пошло не так, попробуйте еще раз.")
    
    elif "размер" in callback.data:
        order += "\n"+food_choice+" "+callback.data+"\n"
        if menu_choice=="Горячие напитки":
            markup = types.InlineKeyboardMarkup(row_width=2)
            dop_btn=[]
            back_btn = types.InlineKeyboardButton(text="Назад", callback_data="back_to_menu")
            for i in dopping:
                dop_btn.append(
                    types.InlineKeyboardButton(text=i,callback_data="dopping "+i)
                )
            not_dop = types.InlineKeyboardButton(text="Без добавок",callback_data="dopping бех сиропа")
            markup.add(*dop_btn,not_dop,back_btn)
            bot.edit_message_text(chat_id=callback.message.chat.id,message_id=callback.message.message_id,text= 'Выберите добавку', reply_markup=markup)
        else:
            get_menu_one(callback.message, "Заказ добавлен")
    

    # ДОПОЛНИТЕЛЬНЫЕ ВОЗМОЖНОСТИ (РАЗМЕР И ДОППИНГ)
    elif callback.data == "ordering" :
     
    
            order += "\n"+food_choice+"\n"
            get_menu_one(callback.message, "Заказ добавлен")
    # ОФОРМЛЕНИЕ ЗАКАЗА С ДОППИНГОИ
    elif "dopping" in callback.data:
        order += "\n"+callback.data+"\n"
        get_menu_one(callback.message, "Заказ добавлен")
    # ВЫБОР РАЗМЕРА НАПИТКА
    elif callback.data == "choice_size":
            markup = types.InlineKeyboardMarkup(row_width=2)
            if "Чай" in food_choice:
                bg_siz = "Чайник"
                sml_siz = "Кружка"
            else:
                bg_siz = "Большой размер"
                sml_siz = "Маленький размер"
            
            big_size = types.InlineKeyboardButton(text=bg_siz, callback_data="Большой размер")
            small_size = types.InlineKeyboardButton(text=sml_siz, callback_data="Маленький размер")
            back_btn = types.InlineKeyboardButton(text="Назад", callback_data="back_to_menu")
            markup.add(big_size,small_size,back_btn)
            bot.edit_message_text(chat_id=callback.message.chat.id,message_id=callback.message.message_id,text= 'Выберите размер', reply_markup=markup)
    
    
    else:
        print("AAAAAAAAAAAAAAAAAAAAAA")


@bot.message_handler(type=["text"])
def get_comment(message):
    global order
    order += "\nКомментарий: " + message.text + "\n"
    print(order)
    #get_menu_one(message, "Комментарий отправлен")
    #bot.register_next_step_handler(message=message,callback=answer_callback)
    start_one(message, "Комментарий добавлен")
bot.polling(non_stop=True, interval=0)