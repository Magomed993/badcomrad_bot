import logging
import os

from dotenv import load_dotenv
from functools import partial
from telegram import Update, Bot
from tg_logger import TelegramLogsHandler
from dialog_flow import detect_intent_texts
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext


logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2('Добро пожаловать\! Это умный бот\.')


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def sends_messages(update: Update, context: CallbackContext, proj_id, language_code) -> None:
    session_id = f'tg - {update.effective_user.id}'
    response_text = detect_intent_texts(proj_id, session_id,  [update.message.text], language_code)
    if response_text:
        update.message.reply_text(response_text)
        logger.info(f'Отправлено сообщение телеграмм-боту: "{update.message.text}" от "{session_id}"')


def main() -> None:
    """Start the bot."""
    load_dotenv()
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
    )
    tg_token = os.environ['TG_TOKEN']
    proj_id = os.environ['PROJECT_ID']
    language_code = os.environ['LANGUAGE']

    loggs_token = os.environ['LOGGER_TOKEN']
    chat_id = os.environ['TG_CHAT_ID']

    log_bot = Bot(token=loggs_token)
    logger.setLevel(logging.INFO)
    log_handler = TelegramLogsHandler(log_bot, chat_id)
    logger.addHandler(log_handler)
    logger.info("Телеграмм-бот 'badcomrad' запущен!")

    updater = Updater(tg_token)

    dispatcher = updater.dispatcher

    try:
        dispatcher.add_handler(CommandHandler("start", start))
        dispatcher.add_handler(CommandHandler("help", help_command))
        handler_with_args = partial(sends_messages, proj_id=proj_id, language_code=language_code)
        dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handler_with_args))

        updater.start_polling()

        updater.idle()
    except Exception as err:
        logger.exception(err)


if __name__ == '__main__':
    main()
