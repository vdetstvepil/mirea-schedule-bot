import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id

import dbFunctions
import parameters
import timeTable


def botListen():
    # Авторизация бота по токену.
    vk_session = vk_api.VkApi(token=parameters.api_key)

    # Вызываем longpoll.
    longpoll = VkLongPoll(vk_session)
    vk = vk_session.get_api()

    # Слушаем longpoll на наличие событий.
    for event in longpoll.listen():
        # Пришло новое сообщение.
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            # Выводим сообщение в консоль.
            print('New message from {}, text = {}'.format(event.user_id, event.text))

            # Отправляем ответное сообщение.
            vk.messages.send(
                user_id=event.user_id,
                random_id=get_random_id(),
                message='Ваш текст принят.'
            )


if __name__ == '__main__':
    dbFunctions.loadDb()
    timeTable.init_timetable()

    botListen()
