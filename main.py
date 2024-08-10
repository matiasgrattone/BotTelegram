import telebot
import sqlite3
from telebot import types
import requests
from openai import OpenAI
import openai
import pandas as pd



OPENAI_API_KEY = ''
TOKEN_TELEBOT = ''
API_KEY_WEATHER = ''
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather?'


bot = telebot.TeleBot(TOKEN_TELEBOT)
clientOpenAI = OpenAI(api_key=OPENAI_API_KEY)

def chatWithIA(prompt:str):
    try:
        chat_completion = clientOpenAI.chat.completions.create(
            modelo="gpt-3.5-turbo",
            mensaje=[
                {"role": "user", 
                    "content": prompt}
            ]
        )
        return chat_completion.choices[0].mensaje.content.strip()
    except Exception as e:
        return "Perdon error en el servidor de openai intente mas tarde"


def insert_new_user(user_id:int,username:str):
    conn = sqlite3.connect('telegram_bot.db')
    cursor = conn.cursor()
    cursor.execute(''' 
        INSERT OR IGNORE INTO users (user_id,username) VALUES (?,?)
    ''',(user_id,username))
    conn.commit()
    cursor.close()
    conn.close()

def insert_user_message(user_id:int,message:str):
    conn = sqlite3.connect('telegram_bot.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE users SET ultima_conversacion = ? WHERE user_id = ?
    ''',(message,user_id))
    conn.commit()
    cursor.close()
    conn.close()

def view_ultima_conversacion(user_id:int):
    try:
        conn = sqlite3.connect('telegram_bot.db')
        cursor = conn.cursor()
        cursor.execute(''' 
            SELECT ultima_conversacion FROM users WHERE user_id = ?
        ''',(user_id,))
        ultima_conversacion = cursor.fetchone()
        cursor.close()
        conn.close()
        return ultima_conversacion[0]
    except Exception as e:
        return "No hay conversaciones anteriores"

def contarBD(user_id:int,username:str):
    conn = sqlite3.connect('telegram_bot.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR IGNORE INTO users (user_id,username) VALUES (?,?)
    ''',(user_id,username))
    cursor.execute('''
        UPDATE users SET contador = contador + 1 WHERE user_id = ?
    ''',(user_id,))
    conn.commit()
    cursor.close()
    conn.close()

def view_contador(user_id:int):
    conn = sqlite3.connect('telegram_bot.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT contador FROM users WHERE user_id = ?
    ''',(user_id,))
    contador = cursor.fetchone()
    cursor.close()
    conn.close()
    return contador[0]


def get_weather(city_name):
    complete_url = BASE_URL + "q=" + city_name + "&lang=es" + "&appid=" + API_KEY_WEATHER
    response = requests.get(complete_url)
    data = response.json()
    if int(data["cod"]) != 404:
        main_data = data["main"]
        weather_data = data["weather"][0]
        temperature = main_data["temp"] - 273.15
        description = weather_data["description"]
        msg = chatWithIA("(sin introducciones y siempre en español)recomendacion larga sobre que hacer en la ciudad de "+city_name +"pais:"+data["sys"]["country"])
        return f"La temperatura en {city_name} es de {temperature:.2f}°C \n{description.capitalize()} \n{chatWithIA('(recomendacion corta 1 oracion , sin introduccion),basada en clima:'+description)} \n{msg}"
    else:
        return 'Ciudad no encontrada'


def contar(message):
    username_id = message.chat.id
    username = message.chat.username
    contarBD(username_id,username)
    bot.send_message(message.chat.id,"Bien haz contado!!!")
    bot.send_message(message.chat.id,f"Haz contado {view_contador(username_id)} veces")


def send_weather(message):
    city_name = message.text
    if city_name:
        weather_info = get_weather(city_name)
        if weather_info == "Ciudad no encontrada":
            bot.reply_to(message,"Ciudad no encontrada")
        else:
            bot.reply_to(message,weather_info)
    else:
        bot.reply_to(message,"Por favor , proporciona el nombre de la cuiudad. Ejemplo: /clima Montevideo")


#MENU DEL BOT
@bot.message_handler(commands=['start'])
def send_welcome(message):
    insert_new_user(message.chat.id,message.chat.username)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    clima_option = types.KeyboardButton(text="¡Quiero saber el clima! \U00002600")
    chat_option = types.KeyboardButton(text="Chat \U0001F4AC")
    chat_analisis = types.KeyboardButton(text="Analisis de sentimientos \U0001F4AC")
    contador = types.KeyboardButton(text="¡Quiero contar! \U0001F522")
    autor = types.KeyboardButton(text="Ver TOP 5 Canciones \U0001F3C6")
    markup.add(clima_option,chat_option,contador,autor,chat_analisis)
    bot.send_message(message.chat.id,"¡Hola! ¿Que Necesitas?",reply_markup=markup)
    


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if(message.text == "¡Quiero saber el clima! \U00002600"):
        msg = bot.send_message(message.chat.id,'Dime la ciudad que queres saber el clima')
        bot.register_next_step_handler(msg, save_user_message,1)
    elif(message.text == "Chat \U0001F4AC"):
        msg = bot.send_message(message.chat.id,'Hola bienvenido al chat, dime que quieres saber?')
        bot.register_next_step_handler(msg, save_user_message,2)
    elif(message.text == "¡Quiero contar! \U0001F522"):
        contar(message)
    elif(message.text == "TOP 5 Canciones \U0001F3C6"):
        msg = bot.send_message(message.chat.id,'Dime el nombre del autor')
        bot.register_next_step_handler(msg, save_user_message,4)
    elif(message.text == "Analisis de sentimientos \U0001F4AC"):
        if(view_ultima_conversacion(message.chat.id) == "No hay conversaciones anteriores"):
            bot.send_message(message.chat.id,"No hay conversaciones anteriores , intenta hablar conmigo usando la opcion Chat\U0001F4AC en el menu")
        else:
            msg = bot.send_message(message.chat.id,'Analizando sentimientos del ultimo chat....chat: "'+view_ultima_conversacion(message.chat.id)+'"')
            msg2 =chatWithIA("(sin introducciones)dime el sentimiento que esta mostrando esta conversacion (positivo,negativo,neutral) y luego dime una explicacion del porque , conversacion:"+view_ultima_conversacion(message.chat.id))
            bot.send_message(message.chat.id,"Analisis de sentimientos completado")
            bot.send_message(message.chat.id,msg2)
    elif(message.text.lower() == "salir"):
        bot.send_message(message.chat.id,"Hasta luego")
    else:
        bot.reply_to(message, "No entiendo lo que me dices")
    


def save_user_message(message,opcion):
    global autor , top1
    if(opcion == 1):
        send_weather(message)
    elif(opcion == 2):
        msg = chatWithIA(message.text)
        insert_new_user(message.chat.id,message.chat.username)
        insert_user_message(message.chat.id,message.text)
        bot.send_message(message.chat.id,msg)
    elif(opcion == 4):
        #esta funcionalidad fue utilizada con la api openai de chat.completions
        # para poder mostrar la curiosidad del top1 se uso splitlines con el resultado de la primer consulta 
        # luego se lo inserto en el prompt para mostrar la curiosidad
        bot.send_message(message.chat.id,"Buscando canciones del artista espere un momento....")
        bot.send_message(message.chat.id,"Estas son las TOP 5 canciones del artista "+message.text+":")
        msg = chatWithIA("(formato lista 1-nombre cancion endline 2-nombre cancion etc,sin introducciones y en español)TOP 5 canciones de "+message.text +"segun popularidad mostrando las reproducciones")
        msg2 = chatWithIA("(Sin introducciones y siempre en español) ,dime una dato cuorioso sobre la cancion "+msg.splitlines()[0] + " de "+message.text)
        bot.send_message(message.chat.id,msg+"\n\ndato curioso:\n"+msg2)
        autor = message.text
        top1 = msg.splitlines()[0]
        #preguntarle al usuario usando keyboardinline si queire ver la letra de la cancion
        markup = types.InlineKeyboardMarkup()
        letra = types.InlineKeyboardButton(text="Ver letra",callback_data="letra")
        markup.add(letra)
        bot.send_message(message.chat.id,"Quieres ver la letra de la cancion top1?",reply_markup=markup)
    else:
        pass

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "letra":
        bot.send_message(call.message.chat.id,"Letra de la cancion:\n"+chatWithIA("(sin introducciones y siempre en español)dime la letra de la cancion "+top1+" de "+autor))
        

bot.polling()
