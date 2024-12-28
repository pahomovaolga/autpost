import logging
import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Replace 'YOUR_BOT_TOKEN' with your actual bot token from BotFather
BOT_TOKEN = 'YOUR_BOT_TOKEN'
CHAT_ID = 'YOUR_CHAT_ID'  # Replace with the chat ID where you want to post

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to fetch content from a website
def fetch_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    # Customize the following line to extract the content you need
    content = soup.find('div', class_='content-class').get_text(strip=True)
    return content

# Function to post content to Telegram
def post_to_telegram(context: CallbackContext):
    url = 'http://example.com'  # Replace with the actual website URL
    content = fetch_content(url)
    context.bot.send_message(chat_id=CHAT_ID, text=content)

# Command to start the bot
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Bot started! Use /post to fetch and post content.')

# Command to manually fetch and post content
def post(update: Update, context: CallbackContext) -> None:
    post_to_telegram(context)

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("post", post))

    # Set up a job to run the post_to_telegram function every hour
    job_queue = updater.job_queue
    job_queue.run_repeating(post_to_telegram, interval=3600, first=0)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
