from datetime import datetime, timedelta

import requests

from project import parameters

# Получить погоду в городе.
def getWeather(city):
    request_str = "http://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid=" + parameters.weather_key \
                  + "&units=metric&&lang=RU"
    response = requests.get(request_str)
    info = response.json()

    w_temperature = int(info["main"]["temp"])
    w_pressure = int(int(info["main"]["pressure"]) / 1.333)
    w_humidity = int(info["main"]["humidity"])
    w_wind_speed = round(info["wind"]["speed"], 1)
    w_wind_direction = degToCompass(int(info["wind"]["deg"]))
    w_wind_descr = speedToDescr(float(info["wind"]["speed"]))
    w_type_weather = ""
    w_description = ""
    w_icon = ""
    for item in info["weather"][:1]:
        w_type_weather = item["main"]
        w_description = str(item["description"]).capitalize()
        w_icon = item["icon"]
    w_icon = iconToSmile(w_icon)

    return "Погода в Москве\n\n" + str(w_icon) + " " + str(w_description) + "\n🌡 Температура: " + str(w_temperature) \
           + "°C\nДавление: " + str(w_pressure) + " мм. рт. ст., влажность: " + str(w_humidity) + "%\nВетер: " + \
           str(w_wind_speed) + " м/c, " + str(w_wind_descr) + ", " + str(w_wind_direction)


# Получить прогноз на сегодня.
def getTodayForecast(city):
    request_str = "http://api.openweathermap.org/data/2.5/forecast?q=" + city + "&appid=" + parameters.weather_key \
                  + "&units=metric&&lang=RU"
    response = requests.get(request_str)
    info = response.json()

    return_str = "Погода в Москве на сегодня"
    for i in info['list']:
        if i['dt_txt'] == (datetime.today()).strftime("%Y-%m-%d") + " 06:00:00" or \
                i['dt_txt'] == (datetime.today()).strftime("%Y-%m-%d") + " 12:00:00" or \
                i['dt_txt'] == (datetime.today()).strftime("%Y-%m-%d") + " 18:00:00" or \
                i['dt_txt'] == (datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d") + " 00:00:00":
            if i['dt_txt'] == (datetime.today()).strftime("%Y-%m-%d") + " 06:00:00":
                return_str = return_str + "\n\nУТРО\n"
            elif i['dt_txt'] == (datetime.today()).strftime("%Y-%m-%d") + " 12:00:00":
                return_str = return_str + "\n\nДЕНЬ\n"
            elif i['dt_txt'] == (datetime.today()).strftime("%Y-%m-%d") + " 18:00:00":
                return_str = return_str + "\n\nВЕЧЕР\n"
            elif i['dt_txt'] == (datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d") + " 00:00:00":
                return_str = return_str + "\n\nНОЧЬ\n"

            w_temperature = int(i["main"]["temp"])
            w_pressure = int(int(i["main"]["pressure"]) / 1.333)
            w_humidity = int(i["main"]["humidity"])
            w_wind_speed = round(i["wind"]["speed"], 1)
            w_wind_direction = degToCompass(int(i["wind"]["deg"]))
            w_wind_descr = speedToDescr(float(i["wind"]["speed"]))
            w_type_weather = ""
            w_description = ""
            w_icon = ""
            for item in i["weather"][:1]:
                w_type_weather = item["main"]
                w_description = str(item["description"]).capitalize()
                w_icon = item["icon"]
            w_icon = iconToSmile(w_icon)
            return_str = return_str + str(w_icon) + " " + str(w_description) + "\n🌡 Температура: " + str(
                w_temperature) \
                         + "°C\nДавление: " + str(w_pressure) + " мм. рт. ст., влажность: " + str(
                w_humidity) + "%\nВетер: " + \
                         str(w_wind_speed) + " м/c, " + str(w_wind_descr) + ", " + str(w_wind_direction)

    return return_str

# Получить погоду на завтра.
def getTomorrowForecast(city):
    request_str = "http://api.openweathermap.org/data/2.5/forecast?q=" + city + "&appid=" + parameters.weather_key \
                  + "&units=metric&&lang=RU"
    response = requests.get(request_str)
    info = response.json()

    return_str = "Погода в Москве на завтра"
    for i in info['list']:
        if i['dt_txt'] == (datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d") + " 06:00:00" or \
                i['dt_txt'] == (datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d") + " 12:00:00" or \
                i['dt_txt'] == (datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d") + " 18:00:00" or \
                i['dt_txt'] == (datetime.today() + timedelta(days=2)).strftime("%Y-%m-%d") + " 00:00:00":
            if i['dt_txt'] == (datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d") + " 06:00:00":
                return_str = return_str + "\n\nУТРО\n"
            elif i['dt_txt'] == (datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d") + " 12:00:00":
                return_str = return_str + "\n\nДЕНЬ\n"
            elif i['dt_txt'] == (datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d") + " 18:00:00":
                return_str = return_str + "\n\nВЕЧЕР\n"
            elif i['dt_txt'] == (datetime.today() + timedelta(days=2)).strftime("%Y-%m-%d") + " 00:00:00":
                return_str = return_str + "\n\nНОЧЬ\n"
            w_temperature = int(i["main"]["temp"])
            w_pressure = int(int(i["main"]["pressure"]) / 1.333)
            w_humidity = int(i["main"]["humidity"])
            w_wind_speed = round(i["wind"]["speed"], 1)
            w_wind_direction = degToCompass(int(i["wind"]["deg"]))
            w_wind_descr = speedToDescr(float(i["wind"]["speed"]))
            w_type_weather = ""
            w_description = ""
            w_icon = ""
            for item in i["weather"][:1]:
                w_type_weather = item["main"]
                w_description = str(item["description"]).capitalize()
                w_icon = item["icon"]
            w_icon = iconToSmile(w_icon)
            return_str = return_str + str(w_icon) + " " + str(w_description) + "\n🌡 Температура: " + str(
                w_temperature) \
                         + "°C\nДавление: " + str(w_pressure) + " мм. рт. ст., влажность: " + str(
                w_humidity) + "%\nВетер: " + \
                         str(w_wind_speed) + " м/c, " + str(w_wind_descr) + ", " + str(w_wind_direction)
    return return_str

# Получить погоду на неделю.
def getWeekForecast(city):
    request_str = "http://api.openweathermap.org/data/2.5/forecast?q=" + city + "&appid=" + parameters.weather_key \
                  + "&units=metric&&lang=RU"
    response = requests.get(request_str)
    info = response.json()

    k = 1
    day_iter = 0
    night_iter = 0
    return_str = "Погода в Москве с " + (datetime.today() + timedelta(days=1)).strftime("%d.%m") + " по " + \
                 (datetime.today() + timedelta(days=6)).strftime("%d.%m") + "\n\n"

    return_day = " "
    return_night = " "
    for i in info['list']:
        if i['dt_txt'] == (datetime.today() + timedelta(days=k)).strftime("%Y-%m-%d") + " 03:00:00":
            night_iter = night_iter + 1
            w_temperature = int(i["main"]["temp"])
            w_icon = ""
            for item in i["weather"][:1]:
                w_icon = item["icon"]
            w_icon = iconToSmile(w_icon)
            return_night = return_night + "/ " + str(w_temperature) + "°C /"
        if i['dt_txt'] == (datetime.today() + timedelta(days=k)).strftime("%Y-%m-%d") + " 15:00:00":
            day_iter = day_iter + 1
            w_temperature = int(i["main"]["temp"])
            w_icon = ""
            for item in i["weather"][:1]:
                w_icon = item["icon"]
            w_icon = iconToSmile(w_icon)
            return_str = return_str +  "/ " + w_icon + " /"
            return_day = return_day + "/ " + str(w_temperature) + "°C /"
            k = k + 1
    if night_iter == 4:
        return_night = return_night + "/ - /"
    if day_iter == 4:
        return_day = return_day + "/ - /"

    return_day = return_day + "&#12288;ДЕНЬ"
    return_night = return_night + "&#12288;НОЧЬ"
    return_str = return_str + "\n\n" + return_night + "\n" + return_day
    return return_str

# Преобразовать иконку в смайлик.
def iconToSmile(icon):
    if icon == "01d":
        return "☀"
    elif icon == "01n":
        return "🌑"
    elif icon == "02d":
        return "⛅"
    elif icon in ("03d", "03n"):
        return "☁🌑"
    elif icon in ("04d", "04n"):
        return "☁☁"
    elif icon in ("09d", "09n"):
        return "🌧"
    elif icon == "10d":
        return "🌦"
    elif icon == "10n":
        return "🌧🌑"
    elif icon in ("11d", "11n"):
        return "⛈"
    elif icon in ("13d", "13n"):
        return "❄"
    elif icon in ("50d", "50n"):
        return "🌫"

# Перевести тип погоды с английского на русский.
def typeWeatherToRus(type_weather):
    if type_weather == "Thunderstorm":
        return "Гроза"
    elif type_weather == "Drizzle":
        return "Моросящий дождь"
    elif type_weather == "Rain":
        return "Дождь"
    elif type_weather == "Snow":
        return "Снег"
    elif type_weather == "Mist":
        return "Туман"
    elif type_weather == "Smoke":
        return "Дым"
    elif type_weather == "Haze":
        return "Легкий туман"
    elif type_weather == "Dust":
        return "Пыль"
    elif type_weather == "Fog":
        return "Туман"
    elif type_weather == "Sand":
        return "Песчаная буря"
    elif type_weather == "Sand":
        return "Пепельная погода"
    elif type_weather == "Squall":
        return "Шквал"
    elif type_weather == "Tornado":
        return "Торнадо"
    elif type_weather == "Clear":
        return "Ясно"
    elif type_weather == "Clouds":
        return "Облачно"
    else:
        return "нет информации"

# Преобразовать градусы в характер ветра.
def degToCompass(num):
    val = int((num / 22.5) + .5)
    arr = ["северный", "северо-восточный", "северо-восточный", "северо-восточный", "восточный", "юго-восточный",
           "юго-восточный", "юго-восточный", "южный", "юго-западный", "юго-западный", "юго-западный", "западный",
           "северо-западный", "северо-западный", "северо-западный"]
    return arr[(val % 16)]

# Преобразовать скорость ветра в описание.
def speedToDescr(num):
    if 0 <= num < 0.3:
        return "штиль"
    elif 0.3 <= num < 1.6:
        return "тихий"
    elif 1.6 <= num < 3.4:
        return "легкий"
    elif 3.4 <= num < 5.5:
        return "слабый"
    elif 5.5 <= num < 8.0:
        return "умеренный"
    elif 8.0 <= num < 10.8:
        return "свежий"
    elif 10.8 <= num < 13.9:
        return "сильный"
    elif 13.9 <= num < 17.2:
        return "крепкий"
    elif 17.2 <= num < 20.8:
        return "очень крепкий"
    elif 20.8 <= num < 24.5:
        return "шторм"
    elif 24.5 <= num < 28.5:
        return "сильный шторм"
    elif 28.5 <= num < 32.7:
        return "жестокий шторм"
    elif num > 32.7:
        return "ураган"
