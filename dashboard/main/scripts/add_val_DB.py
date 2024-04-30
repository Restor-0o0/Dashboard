
import psycopg2
import datetime
import random
import os
from dotenv import load_dotenv
import time
import pytz

# Устанавливаем часовой пояс Новосибирска
novosibirsk_timezone = pytz.timezone('Asia/Novosibirsk')

load_dotenv()

# Функция для добавления записи в таблицу TimeMark
def insert_time_mark(connection, date_time):
    try:
        cursor = connection.cursor()
        cursor.execute('INSERT INTO public.main_timemark("DateTime") VALUES (%s)', (date_time,))
        connection.commit()
        print("Запись добавлена в таблицу TimeMark")
    except psycopg2.Error as e:
        print("Ошибка при добавлении записи в таблицу TimeMark:", e)

# Функция для добавления записи в таблицу DataSens
def insert_data_sens(connection, time_id, sens_id, value):
    try:
        cursor = connection.cursor()
        cursor.execute('INSERT INTO public.main_datasens ("Time_id", "Sens_id", "Value") VALUES (%s, %s, %s)', (time_id, sens_id, value))
        connection.commit()
        print("Запись добавлена в таблицу DataSens")
    except psycopg2.Error as e:
        print("Ошибка при добавлении записи в таблицу DataSens:", e)

# Функция для получения ID всех датчиков
def get_sensor_ids(connection):
    try:
        cursor = connection.cursor()
        cursor.execute('SELECT "ID" FROM public.main_sensor')
        sensor_ids = [row[0] for row in cursor.fetchall()]
        return sensor_ids
    except psycopg2.Error as e:
        print("Ошибка при получении ID датчиков:", e)
        return []

def find_time_mark_id(connection, rounded_time):
    try:
        cursor = connection.cursor()
        cursor.execute('SELECT "ID" FROM public.main_timemark WHERE "DateTime" = %s', (rounded_time,))
        time_mark_id = cursor.fetchone()[0]
        return time_mark_id
    except psycopg2.Error as e:
        print("Ошибка при поиске записи в таблице TimeMark:", e)
        return None



connection = psycopg2.connect(
    dbname='curent',
    user=os.getenv('LOGIN_BD'),
    password=os.getenv('PASSVORD_BD'),
    host='localhost',
    port=''
)
current_time = datetime.datetime.now()
last_time = current_time.replace(second=0, microsecond=0)
print(last_time)
while True:
    # Получаем текущее время
    current_time = datetime.datetime.now()

    # Округляем время до ближайшей десятой минуты
    rounded_time = current_time.replace(second=0, microsecond=0)
    # Проверяем, является ли текущее время кратным 10 минутам
    print(rounded_time)
    if current_time.minute % 10 == 0 and current_time.minute != last_time:
        last_time = current_time.minute
        print('insert')
        # Создаем запись в таблице TimeMark
        insert_time_mark(connection, rounded_time)
        time_mark_id = find_time_mark_id(connection, rounded_time)
        # Получаем ID всех датчиков
        sensor_ids = get_sensor_ids(connection)

        # Добавляем записи в таблицу DataSens для каждого датчика
        for sensor_id in sensor_ids:
            # Здесь предполагается, что значение датчика известно
            insert_data_sens(connection, time_id=time_mark_id, sens_id=sensor_id, value=round(random.uniform(20, 22), 2))
    # Задержка в 50 секунд
    time.sleep(60)
    # Закрываем соединение с базой данных
connection.close()
