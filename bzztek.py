import os
import telebot
from googlesearch import search
import requests

API_KEY = '5865028196:AAEbqby22cx59cWAw1oWK9jSe4IDdWVFeqQ'
OWM_API_KEY = 'Your OpenWeatherMap API Key'

bot = telebot.TeleBot(API_KEY)

@bot.message_handler(commands=['start'])
def greet(message):
    bot.reply_to(message, "Hello, welcome to Bzztek! I'm here to help you. You can try typing /news to get links to the top news on Google.")

@bot.message_handler(commands=['news'])
def news(message):
    query = 'top news'
    links = search(query, num_results=5)  # retrieve the top 5 search results
    for link in links:
        bot.send_message(message.chat.id, link)  # send each link as a separate message

@bot.message_handler(commands=['weather'])
def weather(message):
    # Ask the user for their location
    bot.reply_to(message, "Please enter your location:")

@bot.message_handler(content_types=['text'])
def handle_location(message):
    # Get weather data for the user's location
    try:
        location = message.text
        url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={OWM_API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()
        if data["cod"] == "404":
            bot.send_message(message.chat.id, "Location not found. Please try again.")
        else:
            # Send weather information to the user
            weather_desc = data["weather"][0]["description"]
            temp = data["main"]["temp"]
            feels_like = data["main"]["feels_like"]
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]
            response_message = f"Current weather for {location}: {weather_desc}\nTemperature: {temp}°C\nFeels like: {feels_like}°C\nHumidity: {humidity}%\nWind speed: {wind_speed} m/s"
            bot.send_message(message.chat.id, response_message)
    except:
        bot.send_message(message.chat.id, "Error getting weather information. Please try again.")

bot.polling()