import threading
from datetime import datetime
from random import random

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id

import dbFunctions
import parameters
import timeTable
from project import weather

# Запуск бота.
def botListen():
    print(parameters.OKGREEN + "Bot started" + parameters.ENDC)

    # Авторизация бота по токену.
    vk_session = vk_api.VkApi(token=parameters.api_key)

    # Вызываем longpoll.
    longpoll = VkLongPoll(vk_session)

    vk = vk_session.get_api()

    custom_group_chosen = ""
    rasp = 0
    custom_teacher_chosen = ""

    # Слушаем longpoll на наличие событий.
    for event in longpoll.listen():
        # Пришло новое сообщение.

        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            print(event.text)
            if event.from_chat:
                vk.messages.send(
                    user_id=event.chat_id,
                    random_id=get_random_id(),
                    message='🎄 Произошла ошибка и всех отчислили!'
                )
            elif event.from_user:  # Если написали в ЛС
                # Выводим сообщение в консоль.
                print('New message from {}, text = {}'.format(event.user_id, event.text))

                if rasp == 1:
                    rasp = 2
                else:
                    rasp = 0
                    custom_teacher_chosen = ""

                if str(event.text).upper() == "НАЧАТЬ":
                    # Отправляем ответное сообщение.
                    vk.messages.send(
                        user_id=event.user_id,
                        random_id=get_random_id(),
                        message='⏰ Это бот-помощник с выводом расписания РТУ МИРЭА.'
                                '\nНапишите имя вашей группы, чтобы бот её запомнил :)'
                                '\n\nТакже, в боте предусмотрено несколько команд:'
                                '\n👉 Бот - расписание вашей группы;'
                                '\n👉 Бот [день недели] - быстрый вывод вашего расписания на выбранный день недели;'
                                '\n👉 Бот [имя группы] - быстрый вывод расписания введенной вами группы;'
                                '\n👉 Бот [день недели] [имя группы] - быстрый вывод расписания введенной вами группы на выбранный день недели;'
                                '\n👉 Погода - вывод данных о погоде в Москве;'
                                '\n👉 Найти [имя преподавателя] - расписание преподавателя'
                    )
                elif str(event.text).upper() == "БОТ" or str(event.text).upper() == "КЛАВИАТУРА" or \
                        str(event.text).upper() == "КЛАВА":
                    keyboard = VkKeyboard(one_time=True)
                    keyboard.add_button('На сегодня', color=VkKeyboardColor.POSITIVE)
                    keyboard.add_button('На завтра', color=VkKeyboardColor.NEGATIVE)
                    keyboard.add_line()
                    keyboard.add_button('На эту неделю', color=VkKeyboardColor.PRIMARY)
                    keyboard.add_button('На следующую неделю', color=VkKeyboardColor.PRIMARY)
                    keyboard.add_line()
                    keyboard.add_button('Какая неделя?', color=VkKeyboardColor.SECONDARY)
                    keyboard.add_button('Какая группа?', color=VkKeyboardColor.SECONDARY)
                    vk.messages.send(
                        user_id=event.user_id,
                        random_id=get_random_id(),
                        keyboard=keyboard.get_keyboard(),
                        message='📣 Показать расписание...'
                    )
                elif str(event.text).upper() == "ПОГОДА":
                    keyboard = VkKeyboard(one_time=True)
                    keyboard.add_button('Сейчас', color=VkKeyboardColor.PRIMARY)
                    keyboard.add_button('Сегодня', color=VkKeyboardColor.POSITIVE)
                    keyboard.add_button('Завтра', color=VkKeyboardColor.POSITIVE)
                    keyboard.add_line()  # переход на вторую строку
                    keyboard.add_button('На 5 дней', color=VkKeyboardColor.POSITIVE)
                    vk.messages.send(
                        user_id=event.user_id,
                        random_id=get_random_id(),
                        keyboard=keyboard.get_keyboard(),
                        message='☁ Показать погоду в Москве...'
                    )
                elif str(event.text).upper() == "СЕЙЧАС":
                    vk.messages.send(
                        user_id=event.user_id,
                        random_id=get_random_id(),
                        message=weather.getWeather("moscow")
                    )
                elif str(event.text).upper() == "СЕГОДНЯ":
                    vk.messages.send(
                        user_id=event.user_id,
                        random_id=get_random_id(),
                        message=weather.getTodayForecast("moscow")
                    )
                elif str(event.text).upper() == "ЗАВТРА":
                    vk.messages.send(
                        user_id=event.user_id,
                        random_id=get_random_id(),
                        message=weather.getTomorrowForecast("moscow")
                    )
                elif str(event.text).upper() == "НА 5 ДНЕЙ":
                    vk.messages.send(
                        user_id=event.user_id,
                        random_id=get_random_id(),
                        message=weather.getWeekForecast("moscow")
                    )
                elif str(event.text).upper() == "НА СЕГОДНЯ":
                    if rasp > 0:
                        vk.messages.send(
                            user_id=event.user_id,
                            random_id=get_random_id(),
                            message=timeTable.get_teacher_timetable_today(custom_teacher_chosen)
                        )
                    elif custom_group_chosen != "":
                        vk.messages.send(
                            user_id=event.user_id,
                            random_id=get_random_id(),
                            message=timeTable.get_group_timetable(custom_group_chosen, "today")
                        )
                    elif get_user_groupname(event.user_id) is None:
                        vk.messages.send(
                            user_id=event.user_id,
                            random_id=get_random_id(),
                            message="❌ У тебя не выбрана группа."
                        )
                    else:
                        vk.messages.send(
                            user_id=event.user_id,
                            random_id=get_random_id(),
                            message=timeTable.get_group_timetable(get_user_groupname(str(event.user_id)), "today")
                        )
                    custom_group_chosen = ""
                elif str(event.text).upper() == "НА ЗАВТРА":
                    if rasp > 0:
                        vk.messages.send(
                            user_id=event.user_id,
                            random_id=get_random_id(),
                            message=timeTable.get_teacher_timetable_tomorrow(custom_teacher_chosen)
                        )
                    elif custom_group_chosen != "":
                        vk.messages.send(
                            user_id=event.user_id,
                            random_id=get_random_id(),
                            message=timeTable.get_group_timetable(custom_group_chosen, "tomorrow")
                        )
                    elif get_user_groupname(event.user_id) is None:
                        vk.messages.send(
                            user_id=event.user_id,
                            random_id=get_random_id(),
                            message="❌ У тебя не выбрана группа."
                        )
                    else:
                        vk.messages.send(
                            user_id=event.user_id,
                            random_id=get_random_id(),
                            message=timeTable.get_group_timetable(get_user_groupname(str(event.user_id)), "tomorrow")
                        )
                    custom_group_chosen = ""
                elif str(event.text).upper() == "НА СЛЕДУЮЩУЮ НЕДЕЛЮ":
                    if rasp > 0:
                        vk.messages.send(
                            user_id=event.user_id,
                            random_id=get_random_id(),
                            message=timeTable.get_teacher_timetable_next_week(custom_teacher_chosen)
                        )
                    elif custom_group_chosen != "":
                        vk.messages.send(
                            user_id=event.user_id,
                            random_id=get_random_id(),
                            message=timeTable.get_group_timetable(custom_group_chosen, "nextweek")
                        )
                    elif get_user_groupname(event.user_id) is None:
                        vk.messages.send(
                            user_id=event.user_id,
                            random_id=get_random_id(),
                            message="❌ У тебя не выбрана группа."
                        )
                    else:
                        vk.messages.send(
                            user_id=event.user_id,
                            random_id=get_random_id(),
                            message=timeTable.get_group_timetable(get_user_groupname(str(event.user_id)), "nextweek")
                        )
                    custom_group_chosen = ""
                elif str(event.text).upper() == "НА ЭТУ НЕДЕЛЮ":
                    if rasp > 0:
                        vk.messages.send(
                            user_id=event.user_id,
                            random_id=get_random_id(),
                            message=timeTable.get_teacher_timetable_this_week(custom_teacher_chosen)
                        )
                    elif custom_group_chosen != "":
                        vk.messages.send(
                            user_id=event.user_id,
                            random_id=get_random_id(),
                            message=timeTable.get_group_timetable(custom_group_chosen, "currentweek")
                        )
                    elif get_user_groupname(event.user_id) is None:
                        vk.messages.send(
                            user_id=event.user_id,
                            random_id=get_random_id(),
                            message="❌ У тебя не выбрана группа."
                        )
                    else:
                        vk.messages.send(
                            user_id=event.user_id,
                            random_id=get_random_id(),
                            message=timeTable.get_group_timetable(get_user_groupname(str(event.user_id)), "currentweek")
                        )
                    custom_group_chosen = ""
                elif str(event.text).upper() == "КАКАЯ НЕДЕЛЯ?":
                    vk.messages.send(
                        user_id=event.user_id,
                        random_id=get_random_id(),
                        message="📆 Сейчас идёт " + str(datetime.today().isocalendar()[1] - 5) + " неделя."
                    )
                    custom_group_chosen = ""
                elif str(event.text).upper() == "КАКАЯ ГРУППА?":
                    group_name = get_user_groupname(event.user_id)
                    if custom_group_chosen != "":
                        vk.messages.send(
                            user_id=event.user_id,
                            random_id=get_random_id(),
                            message="✅ Показываю расписание группы " + custom_group_chosen + "."
                        )
                    elif group_name is None:
                        vk.messages.send(
                            user_id=event.user_id,
                            random_id=get_random_id(),
                            message="❌ У тебя не выбрана группа."
                        )
                    else:
                        vk.messages.send(
                            user_id=event.user_id,
                            random_id=get_random_id(),
                            message="✅ Показываю расписание группы " + group_name + "."
                        )
                    custom_group_chosen = ""
                elif str(event.text).upper() == "БОТ ПОНЕДЕЛЬНИК" \
                        or str(event.text).upper() == "БОТ ВТОРНИК" \
                        or str(event.text).upper() == "БОТ СРЕДА" \
                        or str(event.text).upper() == "БОТ ЧЕТВЕРГ" \
                        or str(event.text).upper() == "БОТ ПЯТНИЦА" \
                        or str(event.text).upper() == "БОТ СУББОТА" \
                        or str(event.text).upper() == "БОТ ВОСКРЕСЕНЬЕ":
                    vk.messages.send(
                        user_id=event.user_id,
                        random_id=get_random_id(),
                        message=timeTable.get_group_timetable(get_user_groupname(str(event.user_id)),
                                                              str(event.text).lower().split(' ')[1])
                    )
                elif "БОТ ПОНЕДЕЛЬНИК" in str(event.text).upper() \
                        or "БОТ ВТОРНИК" in str(event.text).upper() \
                        or "БОТ СРЕДА" in str(event.text).upper() \
                        or "БОТ ЧЕТВЕРГ" in str(event.text).upper() \
                        or "БОТ ПЯТНИЦА" in str(event.text).upper() \
                        or "БОТ СУББОТА" in str(event.text).upper() \
                        or "БОТ ВОСКРЕСЕНЬЕ" in str(event.text).upper():
                    if len(str(event.text).upper().split(" ")) == 3 and \
                            timeTable.findGroup((str(event.text).upper().split(" "))[2]) is True:
                        vk.messages.send(
                            user_id=event.user_id,
                            random_id=get_random_id(),
                            message=timeTable.get_group_timetable(str(event.text).upper().split(" ")[2],
                                                                  str(event.text).lower().split(' ')[1])
                        )
                elif (str(event.text).upper().split(" "))[0] == "БОТ" and len((str(event.text).upper().split(" "))) == 2 \
                        and timeTable.findGroup((str(event.text).upper().split(" "))[1]) is True:
                    keyboard = VkKeyboard(one_time=True)
                    keyboard.add_button('На сегодня', color=VkKeyboardColor.POSITIVE)
                    keyboard.add_button('На завтра', color=VkKeyboardColor.NEGATIVE)
                    keyboard.add_line()  # переход на вторую строку
                    keyboard.add_button('На эту неделю', color=VkKeyboardColor.PRIMARY)
                    keyboard.add_button('На следующую неделю', color=VkKeyboardColor.PRIMARY)
                    keyboard.add_line()  # переход на вторую строку
                    keyboard.add_button('Какая неделя?', color=VkKeyboardColor.SECONDARY)
                    keyboard.add_button('Какая группа?', color=VkKeyboardColor.SECONDARY)
                    vk.messages.send(
                        user_id=event.user_id,
                        random_id=get_random_id(),
                        keyboard=keyboard.get_keyboard(),
                        message="📣 Показать расписание для группы " + (str(event.text).upper().split(" "))[1] + "..."
                    )
                    custom_group_chosen = (str(event.text).upper().split(" "))[1]
                elif (str(event.text).upper().split(" "))[0] == "НАЙТИ" and len(
                        (str(event.text).upper().split(" "))) == 2:
                    teacher = (str(event.text).upper().split(" "))[1]
                    if len(timeTable.get_teachers(teacher)) == 0:
                        vk.messages.send(
                            user_id=event.user_id,
                            random_id=get_random_id(),
                            message="❌ Преподаватель не найден"
                        )
                    elif len(timeTable.get_teachers(teacher)) == 1:
                        keyboard = VkKeyboard(one_time=True)
                        keyboard.add_button('На сегодня', color=VkKeyboardColor.POSITIVE)
                        keyboard.add_button('На завтра', color=VkKeyboardColor.NEGATIVE)
                        keyboard.add_line()  # переход на вторую строку
                        keyboard.add_button('На эту неделю', color=VkKeyboardColor.PRIMARY)
                        keyboard.add_button('На следующую неделю', color=VkKeyboardColor.PRIMARY)
                        vk.messages.send(
                            user_id=event.user_id,
                            random_id=get_random_id(),
                            message="📣 Показать расписание преподавателя " + timeTable.get_teachers(teacher)[0],
                            keyboard=keyboard.get_keyboard()
                        )
                        rasp = 1
                        custom_teacher_chosen = timeTable.get_teachers(teacher)[0]
                    elif len(timeTable.get_teachers(teacher)) > 1:
                        keyboard = VkKeyboard(one_time=True)
                        for i in range(0, len(timeTable.get_teachers(teacher))):
                            keyboard.add_button("Выбрать " + timeTable.get_teachers(teacher)[i],
                                                color=VkKeyboardColor.PRIMARY)
                            if i + 1 != len(timeTable.get_teachers(teacher)):
                                keyboard.add_line()
                        vk.messages.send(
                            user_id=event.user_id,
                            random_id=get_random_id(),
                            keyboard=keyboard.get_keyboard(),
                            message="🔎 Найдено несколько преподавателей. Какой преподаватель вам нужен?"
                        )
                elif (str(event.text).upper().split(" "))[0] == "ВЫБРАТЬ" and len(
                        (str(event.text).upper().split(" "))) == 3:
                    keyboard = VkKeyboard(one_time=True)
                    keyboard.add_button('На сегодня', color=VkKeyboardColor.POSITIVE)
                    keyboard.add_button('На завтра', color=VkKeyboardColor.NEGATIVE)
                    keyboard.add_line()  # переход на вторую строку
                    keyboard.add_button('На эту неделю', color=VkKeyboardColor.PRIMARY)
                    keyboard.add_button('На следующую неделю', color=VkKeyboardColor.PRIMARY)
                    vk.messages.send(
                        user_id=event.user_id,
                        random_id=get_random_id(),
                        message="📣 Показать расписание преподавателя " + (
                                (str(event.text).upper().split(" "))[1] + " " +
                                (str(event.text).upper().split(" "))[2]).title() + "..",
                        keyboard=keyboard.get_keyboard()
                    )
                    rasp = 1
                    custom_teacher_chosen = (str(event.text).upper().split(" "))[1] + " " + \
                                            (str(event.text).upper().split(" "))[2]
                else:
                    if timeTable.findGroup(str(event.text).upper()) is True:
                        sqlite_connection = dbFunctions.sqlite_connection
                        cursor = sqlite_connection.cursor()
                        command = "DELETE FROM users WHERE id = " + str(event.user_id) + ";"
                        cursor.execute(command)
                        command = "INSERT INTO users (id, group_name) VALUES (" + str(event.user_id) + ", \'" + str(
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
                        if (str(event.text).upper().find("ИАБО-") != -1 or str(event.text).upper().find(
                                "ИВБО-") != -1 or str(
                            event.text).upper().find("ИКБО-") != -1 or str(event.text).upper().find(
                            "ИМБО-") != -1 or str(
                            event.text).upper().find("ИНБО-") != -1) and len(str(event.text)) == 10:
                            vk.messages.send(
                                user_id=event.user_id,
                                random_id=get_random_id(),
                                message='❌ Неверная команда.\nЕсли ты хотел указать название своей группы, то тебя и '
                                        'твоих одногруппников вероятно уже отчислили за плохое поведение 🤷‍♂'
                            )
                        else:
                            vk.messages.send(
                                user_id=event.user_id,
                                random_id=get_random_id(),
                                message='❌ Неверная команда.'
                            )

# Получить группу по номеру пользователя.
def get_user_groupname(user_id):
    sqlite_connection = dbFunctions.sqlite_connection
    cursor = sqlite_connection.cursor()
    command = "SELECT group_name FROM users WHERE id = " + str(user_id) + ";"
    cursor.execute(command)
    try:
        return str(cursor.fetchone()[0])
    except:
        return None


if __name__ == '__main__':
    dbFunctions.loadDb()
    timeTable.init_timetable()
    botListen()
