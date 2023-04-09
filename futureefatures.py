# @bot.message_handler(commands=['weather'])
# def weather(message):
#     # Ask the user for their location
#     bot.reply_to(message, "Please enter your location:")

# @bot.message_handler(content_types=['text'])
# def handle_location(message):
#     # Get weather data for the user's location
#     try:
#         location = message.text
#         url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={OWM_API_KEY}&units=metric"
#         response = requests.get(url)
#         data = response.json()
#         if data["cod"] == "404":
#             bot.send_message(message.chat.id, "Location not found. Please try again.")
#         else:
#             # Send weather information to the user
#             weather_desc = data["weather"][0]["description"]
#             temp = data["main"]["temp"]
#             feels_like = data["main"]["feels_like"]
#             humidity = data["main"]["humidity"]
#             wind_speed = data["wind"]["speed"]
#             response_message = f"Current weather for {location}: {weather_desc}\nTemperature: {temp}°C\nFeels like: {feels_like}°C\nHumidity: {humidity}%\nWind speed: {wind_speed} m/s"
#             bot.send_message(message.chat.id, response_message)
#     except:
#         bot.send_message(message.chat.id, "Error getting weather information. Please try again.")

import telebot
import json
import urllib.request
import time
import requests

# This library will be used to parse the JSON data returned by the API.
API_KEY = 'YOUR_TELEGRAM_BOT_TOKEN'
bot = telebot.TeleBot(API_KEY)

gnews_apikey = "YOUR_GNEWS_API_KEY"
url = f"https://gnews.io/api/v4/search?q=example&lang=en&country=us&max=10&apikey={gnews_apikey}"

# Create a log file to store all messages
log_file = open('message_log.txt', 'a')

# Define a function to get the latest news
def get_news():
    # Wrap the API call in a try-except block to catch any errors
    try:
        # Use the requests library to make the API call and get the response
        response = requests.get(url)
        # If the response was successful, parse the JSON data and return the articles
        if response.status_code == 200:
            data = response.json()
            articles = data["articles"]
            return articles
        # If the response was not successful, print an error message and return an empty list
        else:
            print(f"Error: {response.status_code} - {response.reason}")
            return []
    # If an error occurred during the API call, print an error message and return an empty list
    except Exception as e:
        print(f"Error: {e}")
        return []

# Call the function to get the initial articles
articles = get_news()

# Define a function to send the news articles to the user
def send_news(chat_id):
    # Get the latest articles
    articles = get_news()
    # If there are articles, send them to the user
    if articles:
        for article in articles:
            title = article['title']
            description = article['description']
            url = article['url']
            message_text = f"<b><i><a href='{url}'>{title}</a></i></b>\n\n{description}"
            bot.send_message(chat_id, message_text, parse_mode='HTML')
    # If there are no articles, send a message to the user
    else:
        bot.send_message(chat_id, "Sorry, there are no news articles at the moment.")

# Define a function to handle the /start command
@bot.message_handler(commands=['start'])
def greet(message):
    bot.reply_to(message, "Hello, welcome to Bzztek! I'm here to help you. You can try typing /news to get links to the top news on Google.")

# Define a function to handle the /news command
@bot.message_handler(commands=['news'])
def news(message):
    # Call the function to send the news articles to the user
    send_news(message.chat.id)

# Define a function to log all messages
@bot.message_handler(func=lambda message: True)
def log_messages(message):
    user = message.from_user.username if message.from_user.username else message.from_user.first_name  # Get the user's username or first name
    text = message.text  # Get the text of the message
    log_file.write(f'{user}: {text}\n')  # Write the message to the log file

    # You can also do other things with the message, like processing it or responding to it
    # ...

    # Echo back the message
    # bot.send_message(message.chat.id, f"You said: {text}")
    print(f'{user}: {text}')

# Set the polling interval to 1 second to prevent the request from taking down the app
bot.polling(none)