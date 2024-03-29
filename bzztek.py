import os
import requests
import telebot
import wikipedia
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import subprocess
import datetime
from telebot import types
import time

load_dotenv()

API_KEY = os.getenv('API_KEY')
bot = telebot.TeleBot(API_KEY)

gnews_apikey = os.getenv('gnews_apikey')
url = f"https://gnews.io/api/v4/search?q=example&lang=en-ph&country=ph&max=5&apikey={gnews_apikey}"

# Create a log file to store all messages
log_file = open('message_log.txt', 'a', encoding='utf-8')

app_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

# Get top 5 articles from the news API
response = requests.get(url)
if response.status_code == 200:
    data = response.json()
    articles = data["articles"]
else:
    articles = []

@bot.message_handler(commands=['start'])
def greet(message):
    bot.reply_to(message, "Hello, welcome to Bzztek! I'm here to help you. Here are the available commands:\n\n"
                          "/news - Get links to the top news on Google.\n"
                          "/wiki - Search for a topic on Wikipedia.\n"
                          "/help - Show this list of available commands.")

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, "Here are the available commands:\n\n"
                                      "/news - Get links to the top news on Google.\n"
                                      "/wiki - Search for a topic on Wikipedia.\n"
                                      "/help - Show this list of available commands.")
    
@bot.message_handler(commands=['browser'])
def help(message):
    bot.send_message(message.chat.id, "Opening the browser...\n\n")
    subprocess.Popen([app_path, "https://www.google.com/"])

# @bot.message_handler(commands=['time'])
# def send_time_periodically(message):
#     while True:
#         # Get the current time and format it
#         current_time = datetime.datetime.now().strftime('%H:%M:%S')
#         # Send the time to the user
#         bot.send_message(message.chat.id, f"The current time is {current_time}")
#         # Wait for 1 minute
#         # time.sleep(60)

@bot.message_handler(commands=['wiki'])
def wiki(message):
    try:
        if len(message.text.split('/wiki ')) != 2:
            bot.send_message(message.chat.id, "Invalid command syntax. Please use the format: /wiki (search_query)")
            return

        query = message.text.split('/wiki ')[1]
        summary = wikipedia.summary(query, sentences=2)
        bot.send_message(message.chat.id, summary)
    except wikipedia.exceptions.PageError:
        bot.send_message(message.chat.id, "Sorry, I could not find any information on that topic.")
    except wikipedia.exceptions.DisambiguationError as e:
        options = "\n".join(e.options[:5])  # show the top 5 suggestions
        bot.send_message(message.chat.id, f"Please be more specific. Did you mean one of these?\n\n{options}")

@bot.message_handler(commands=['news'])
def news(message):
    try:
        for article in articles:
            title = article['title']
            description = article['description']
            url = article['url']
            message_text = f"<b><i><a href='{url}'>{title}</a></i></b>\n\n{description}"
            bot.send_message(message.chat.id, message_text, parse_mode='HTML')
    except requests.exceptions.ConnectionError:
        bot.send_message(message.chat.id, "Sorry, there was an error connecting to the news source. Please try again later.")

@bot.message_handler(func=lambda message: True)
def log_messages(message):
    user = message.from_user.username if message.from_user.username else message.from_user.first_name  # Get the user's username or first name
    text = message.text  # Get the text of the message
    log_file.write(f'{user}: {text}\n')  # Write the message to the log file

    # bot.send_message(message.chat.id, f"You said: {text}")
    print(f'{user}: {text}')

print('Bot is running...')
bot.polling()