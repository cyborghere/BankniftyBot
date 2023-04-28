import os
import requests
from bs4 import BeautifulSoup
import telegram
from telegram.ext import CommandHandler, Updater

# Fetch Telegram bot token from environment variable
token = os.environ['TELEGRAM_BOT_TOKEN']
bot = telegram.Bot(token)

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to the ITM Limited strike price bot. Type /strike to get the latest strike price.")

def strike(update, context):
    # Fetch the latest ITM Limited strike price from the NSE website
    page = requests.get('https://www.nseindia.com/get-quotes/equity?symbol=ITM&illiquid=0&smeFlag=0&itpFlag=0')
    soup = BeautifulSoup(page.content, 'html.parser')
    strike_price = soup.find('div', {'class': 'quoteLtp'}).text.strip()

    # Send the strike price as a message to the user
    context.bot.send_message(chat_id=update.effective_chat.id, text="The latest strike price of ITM Limited is " + strike_price)

updater = Updater(token, use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('strike', strike))
updater.start_polling()
