# BotTelegram

Este repositorio contiene el codigo para crear un bot de telegram con las funcionalidades de clima , contar , hablar con el bot , Analisis de sentimientos y TOP 5 canciones de un cantante


##  Configuracion
  * Clona este repositorio.
  * Instala las dependencias usando `pip install -r requirements.txt`.
  * Crea un bot en telegram a travez de BotFather y obten tu token.
  * Remplaza el token en `main.py` con tu token.
  * Ejecuta el bot usando `python main.py`.

## Funcionalidades
El bot reconoce el comando /start , luego se mostrara un menu de botones donde tendran las siguientes opciones:
* Consultar el clima:
   * Mostrara la temperatura , el clima , una recomendacion basada en el clima y una recomendacion de que hacer en la ciudad indicada.
* Hablar con el bot:
  * Podras comunicarte con el bot para hacerle las preguntas que quieras.
* Contar:
  * El bot llevara una cuenta de cuantas veces haz contado empezando desde 1.
* Analisis de sentimientos:
  * El bot analizara el anterior chat del usuario con el bot y mostrara si fue positivo,negativo o neutral y una pequeña explicacion del porque.
* TOP 5 canciones:
  * Introducciendo a un autor podras ver sus top 5 canciones mas populares , una curiosidad sobre la mas escuchada y la opcion si el usuario quiere de ver la letra de la cancion.

## Conexión con APIs
  * Este bot utiliza las APIs de OpenWeatherMap y openai para proporcionar informacion meteorológica en tiempo real y respuestas inteligentes a tus pedidos respectivamente. Asegúrate de obtener tu propia clave API de OpenWeatherMap
y openai y remplazarlas `API_KEY_WEATHER` y `OPENAI_API_KEY` en `main.py` con tus claves.



##  Funcionalidad Libre:
  * Me decidí por poner la funcionalidad musica y letra al bot porque me parecia interesante poder mostrar una top de canciones y poder ver las letras de las canciones, utilizando la api de openai el bot puede detectar el autor que el usuario le pide y le mostrara sus top 5 canciones junto a una pequeña curiosidad de la cancion mas popular , además si el usuario lo requiere puede preguntar por la letra de la canción mas escuchada.
