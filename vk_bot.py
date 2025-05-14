import os
import random
import vk_api
import logging

from telegram import Bot
from tg_logger import TelegramLogsHandler
from dotenv import load_dotenv
from vk_api.longpoll import VkLongPoll, VkEventType
from dialog_flow import detect_intent_texts


logger = logging.getLogger(__name__)


def smart_guy(event, vk_api):
    proj_id = os.environ['PROJECT_ID']
    session_id = random.randint(100000000, 999999999)
    language_code = os.environ['LANGUAGE']
    response_text = detect_intent_texts(proj_id, session_id, [event.text], language_code)
    if response_text:
        vk_api.messages.send(
            user_id=event.user_id,
            message=response_text,
            random_id=random.randint(1,1000)
        )
        logger.info(f'Отправлено сообщение ВК-сообществу: "{event.text}"')


if __name__ == "__main__":
    load_dotenv()
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
    )
    vk_token = os.environ['VK_TOKEN']
    vk_session = vk_api.VkApi(token=vk_token)

    loggs_token = os.environ['LOGGS_TOKEN']
    chat_id = os.environ['CHAT_ID']

    log_bot = Bot(token=loggs_token)
    logger.setLevel(logging.INFO)
    log_handler = TelegramLogsHandler(log_bot, chat_id)
    logger.addHandler(log_handler)
    logger.info("ВК-сообщество 'test_group' запущен!")

    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    try:
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                smart_guy(event, vk_api)
    except Exception as err:
        logger.exception(err)
