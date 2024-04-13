import telebot  # Импортируем модуль telebot из библиотеки pyTelegramBotAPI.
import requests  # Импортируем модуль requests для выполнения HTTP-запросов.


def get_country_info(country: str):  # Определяем функцию для получения информации о стране.
    url = f"https://restcountries.com/v2/name/{country}"  # Формируем URL для запроса информации о стране.
    response = requests.get(url)  # Выполняем GET-запрос к API.
    data = response.json()[0]  # Преобразуем ответ от API в JSON и берем первый элемент списка.
    return data  # Возвращаем полученные данные.


bot = telebot.TeleBot('7116130817:AAHSW0J7j-k5wA8iGdGfUN3XU8TwXl21nvY')  # Создаем экземпляр класса TeleBot, используя ваш API-ключ.


@bot.message_handler(content_types=['text'])  # Определяем обработчик сообщений для текстовых сообщений.
def get_text_messages(message):  # Определяем функцию для обработки текстовых сообщений.
    if message.text == '/country':  # Если текст сообщения равен '/country'...
        bot.send_message(message.from_user.id,
                         "Введите название страны 🌍")  # ...просим пользователя ввести название страны.
        bot.register_next_step_handler(message,
                                       get_country_info_bot)  # Регистрируем обработчик следующего шага, который вызовет функцию get_country_info_bot.
    else:  # Если текст сообщения не равен '/country'...
        bot.send_message(message.from_user.id, 'Напишите 🌍 /country')  # ...просим пользователя написать '/country'.


def get_country_info_bot(message):  # Определяем функцию для получения информации о стране.
    country = message.text  # Получаем текст сообщения, который является названием страны.
    try:  # Пытаемся...
        data = get_country_info(country)  # ...получить информацию о стране.
        bot.send_message(message.from_user.id,
                         f'Страна: {data["name"]}\n'  # ...отправить сообщение с информацией о стране.
                         f'Столица: {data["capital"]}\n'
                         f'Население: {data["population"]}\n'
                         f'Площадь: {data["area"]} км²\n'
                         f'Регион: {data["region"]}')
        bot.send_message(message.from_user.id,
                         "Введите название страны")  # ...просим пользователя ввести название другой страны.
        bot.register_next_step_handler(message,
                                       get_country_info_bot)  # Регистрируем обработчик следующего шага, который снова вызовет функцию get_country_info_bot.
    except Exception:  # Если произошла ошибка...
        bot.send_message(message.from_user.id,
                         'ПРОИЗОШЛА ОШИБКА...ТАКОЙ СТРАНЫ НЕТУ В БАЗЕ, ПАПРОБУЙТЕ ЕЩЁ РАЗ')  # ...сообщаем об этом пользователю.
        bot.send_message(message.from_user.id,
                         "Введите название страны")  # ...просим пользователя ввести название страны снова.
        bot.register_next_step_handler(message,
                                       get_country_info_bot)  # Регистрируем обработчик следующего шага, который снова вызовет функцию get_country_info_bot.


bot.polling(none_stop=True)  # Запускаем бота.
