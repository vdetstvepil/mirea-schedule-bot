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

            if str(event.text).upper() == "НАЧАТЬ":
                # Отправляем ответное сообщение.
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message='⏰ Это бот-помощник с выводом расписания РТУ МИРЭА.\nПожалуйста, напишите имя вашей группы.'
                )
            else:
                if timeTable.findGroup(str(event.text).upper()) is True:
                    sqlite_connection = dbFunctions.sqlite_connection
                    cursor = sqlite_connection.cursor()
                    command = "DELETE FROM users WHERE id = " + str(event.user_id) + ";"
                    cursor.execute(command)
                    command = "INSERT INTO users VALUES (" + str(event.user_id) + ", \'" + str(
                        event.text).upper() + "\');"
                    cursor.execute(command)
                    vk.messages.send(
                        user_id=event.user_id,
                        random_id=get_random_id(),
                        message='✅ Я запомнил, что ты из группы ' + str(event.text).upper() + '!'
                    )
                    sqlite_connection.commit()
                    cursor.close()
                else:
                    if (str(event.text).upper().find("ИАБО-") != -1 or str(event.text).upper().find("ИВБО-") != -1 or str(
                            event.text).upper().find("ИКБО-") != -1 or str(event.text).upper().find("ИМБО-") != -1 or str(
                                event.text).upper().find("ИНБО-") != -1) and len(str(event.text)) == 10:
                        vk.messages.send(
                            user_id=event.user_id,
                            random_id=get_random_id(),
                            message='❌ Неверная команда.\nЕсли вы хотели указать название своей группы, то вас и '
                                    'студентов вашей группы вероятно отчислили за плохое поведение. 🤷‍♂'
                        )
                    else:
                        vk.messages.send(
                            user_id=event.user_id,
                            random_id=get_random_id(),
                            message='❌ Неверная команда.'
                        )




# def bot_show_timetable_btns():


if __name__ == '__main__':
    dbFunctions.loadDb()
    timeTable.init_timetable()

    botListen()
