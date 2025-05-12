import os
import random
import vk_api

from dotenv import load_dotenv
from vk_api.longpoll import VkLongPoll, VkEventType
from dialodFlow import detect_intent_texts


def echo(event, vk_api):
    proj_id = os.environ['PROJECT_ID']
    session_id = '123456789'
    language_code = os.environ['LANGUAGE']
    vk_api.messages.send(
        user_id=event.user_id,
        message=detect_intent_texts(proj_id, session_id, [event.text], language_code),
        random_id=random.randint(1,1000)
    )


if __name__ == "__main__":
    load_dotenv()
    vk_token = os.environ['VK_TOKEN']
    vk_session = vk_api.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            echo(event, vk_api)
