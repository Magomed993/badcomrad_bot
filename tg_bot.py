import logging
import os

from dotenv import load_dotenv
from telegram import Update, ForceReply
from dialodFlow import detect_intent_texts
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2('Здравствуйте')


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def smart_guy(update: Update, context: CallbackContext) -> None:
    proj_id = os.environ['PROJECT_ID']
    session_id = '123456789'
    language_code = os.environ['LANGUAGE']
    response_text = detect_intent_texts(proj_id, session_id,  [update.message.text], language_code)
    if response_text:
        update.message.reply_text(response_text)


def main() -> None:
    """Start the bot."""
    load_dotenv()
    talkative_token = os.environ['TOKEN']

    updater = Updater(talkative_token)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, smart_guy))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
