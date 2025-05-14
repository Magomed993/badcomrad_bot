import logging
import os
import random

from dotenv import load_dotenv
from telegram import Update, Bot
from dialog_flow import detect_intent_texts
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


class TelegramLogsHandler(logging.Handler):

    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2('Добро пожаловать\! Это умный бот\.')


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def smart_guy(update: Update, context: CallbackContext) -> None:
    proj_id = os.environ['PROJECT_ID']
    session_id = random.randint(100000000, 999999999)
    language_code = os.environ['LANGUAGE']
    response_text = detect_intent_texts(proj_id, session_id,  [update.message.text], language_code)
    if response_text:
        update.message.reply_text(response_text)
        logger.info(f'Отправлено сообщение телеграмм-боту: "{update.message.text}"')


def main() -> None:
    """Start the bot."""
    load_dotenv()
    talkative_token = os.environ['TOKEN']

    loggs_token = os.environ['LOGGS_TOKEN']
    chat_id = os.environ['CHAT_ID']

    log_bot = Bot(token=loggs_token)
    logger.setLevel(logging.INFO)
    log_handler = TelegramLogsHandler(log_bot, chat_id)
    logger.addHandler(log_handler)
    logger.info("Телеграмм-бот 'badcomrad' запущен!")

    updater = Updater(talkative_token)

    dispatcher = updater.dispatcher

    try:
        dispatcher.add_handler(CommandHandler("start", start))
        dispatcher.add_handler(CommandHandler("help", help_command))

        dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, smart_guy))

        updater.start_polling()

        updater.idle()
    except Exception as err:
        logger.exception(err)


if __name__ == '__main__':
    main()
