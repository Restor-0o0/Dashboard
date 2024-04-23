import base64
from io import BytesIO
import numpy as np
import matplotlib.pyplot as plt
from django.http import HttpResponse
from django.shortcuts import render
from PIL import Image


def graph1_func():

    fig, ax = plt.subplots()
    # Изменяем цвет фона
    # Изменяем цвет осей
    ax.spines['bottom'].set_color('gray')
    ax.spines['top'].set_color('gray')
    ax.spines['right'].set_color('gray')
    ax.spines['left'].set_color('gray')

    # Изменяем цвет делений на осях
    ax.tick_params(axis='x', colors='gray')
    ax.tick_params(axis='y', colors='gray')

    # Создаем график с заданным цветом
    x = [1, 2, 3, 4, 5]
    y = [10, 20, 25, 30, 35]
    ax.plot(x, y, color='green', label='График')

    # Добавляем легенду
    ax.legend()
    buffer = BytesIO()

    # Отображаем график
    plt.figure(figsize=(10, 5))
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image = Image.open(buffer)

    def replace_colors_above_threshold(image_path, threshold, new_color_):
        # Открываем изображение
        # Получаем массив NumPy из изображения
        #image_array = np.array(image_path)
        image_array = np.array(image_path)
        # Находим пиксели, которые превышают порог
        c = 0
        for i in image_array:
            for j in i:
                if np.all(j > threshold):
                    j[0] = new_color_[0]
                    j[1] = new_color_[1]
                    j[2] = new_color_[2]
                    j[3] = new_color_[3]

        print(c)
        '''above_threshold = np.all(image_array > threshold, axis=-1)

        # Заменяем цвета, превышающие порог, на новый цвет
        image_array[above_threshold] = new_color_

        # Создаем новый объект Image из массива'''
        new_image = Image.fromarray(image_array)


        return new_image

    # Путь к вашему изображению

    # Порог для замены цветов (например, порог RGB [200, 200, 200])
    threshold_color = [220, 220, 220,220]

    # Новый цвет для замены
    new_color = np.array([9, 56, 65,50])  # Например, красный цвет

    # Заменяем цвета, превышающие порог, на новый цвет
    result_image = replace_colors_above_threshold(image, threshold_color, new_color)
    result_image = replace_colors_above_threshold(result_image, threshold_color, new_color)
    result_image.save('img.png')
    # Создаем словарь для подсчета количества пикселей каждого цвета
    '''pixel_count = {}

    # Подсчитываем количество пикселей каждого цвета
    for pixel in pixels:
        if pixel in pixel_count:
            pixel_count[pixel] += 1
        else:
            pixel_count[pixel] = 1

    # Выводим результат
    for color, count in pixel_count.items():
        print(f"Цвет {color}: {count} пикселей")'''
    buf = BytesIO()
    result_image.save(buf, format='PNG')
    # Возвращение графика в ответе Django
    image_data = buf.getvalue()
    graph = base64.b64encode(image_data)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph


def graph2_func():
    x = [17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28]
    y = [21, 22, 21, 20, 21, 21, 21, 22, 21, 20, 21, 21]

    plt.figure(figsize=(10, 5))
    w = 0.5
    plt.bar(x, y, width=w)
    plt.ylim(15, 35)
    # Ваши данные для построения графика
    # Создание графика

    # Сохранение графика в байтовом массиве
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Возвращение графика в ответе Django
    image_data = buffer.getvalue()
    graph = base64.b64encode(image_data)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph


def graph3_func():
    x = [1, 2, 3, 4, 5]
    y = [10, 20, 25, 30, 35]
    plt.switch_backend('AGG')
    plt.figure(figsize=(10, 5))

    plt.xticks(rotation=180)

    plt.tight_layout()
    # Ваши данные для построения графика

    # Создание графика
    plt.plot(x, y)
    plt.title('My Chart')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')

    # Сохранение графика в байтовом массиве
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Возвращение графика в ответе Django
    image_data = buffer.getvalue()
    graph = base64.b64encode(image_data)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph


''' 
   x = [17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28]
    y = [21, 22, 21, 20, 21, 21, 21, 22, 21, 20, 21, 21]
    plt.figure(figsize=(10, 5))
    plt.xticks(rotation=180)

    plt.tight_layout()
    # Ваши данные для построения графика

    # Создание графика

    plt.title('Температура за неделю')
    plt.xlabel('День')
    plt.ylabel('Температура')
    plt.ylim(15, 35)
    # Сохранение графика в байтовом массиве
    plt.plot(x, y)
    buffer = BytesIO()
    gr = plt.gcf()

    gr.set_facecolor('#093841')
    ax = plt.gca()
    ax.spines['bottom'].set_color('#FFF')
    ax.spines['top'].set_color('#FFF')
    ax.spines['right'].set_color('#FFF')
    ax.spines['left'].set_color('#FFF')
    ax.tick_params(axis='x', colors='#FFF')
    ax.tick_params(axis='y', colors='#FFF')
    gr.savefig(buffer, format='png')
    buffer.seek(0)

    # Возвращение графика в ответе Django
    image_data = buffer.getvalue()
    graph = base64.b64encode(image_data)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph'''
