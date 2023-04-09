from dotenv import load_dotenv
import os
import telebot
from telebot import types
import json
import urllib.request
import requests
import wikipedia
# This library will be used to parse the JSON data returned by the API.

load_dotenv()
API_KEY = os.getenv('API_KEY')
bot = telebot.TeleBot(API_KEY)

gnews_apikey = os.getenv('gnews_apikey')
url = f"https://gnews.io/api/v4/search?q=example&lang=en-ph&country=ph&max=5&apikey={gnews_apikey}"

# Create a log file to store all messages
log_file = open('message_log.txt', 'a', encoding='utf-8')

# Create a log file to store all users
log_file = open('user_log.txt', 'a')

# Get all updates received by the bot
updates = bot.get_updates()

with urllib.request.urlopen(url) as response:
    data = json.loads(response.read().decode("utf-8"))
    articles = data["articles"]

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