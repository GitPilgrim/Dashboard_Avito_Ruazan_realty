#!/usr/bin/env python
# coding: utf-8

import requests
from bs4 import BeautifulSoup
import csv
from pymystem3 import Mystem
import pandas as pd
import re
import datetime
from datetime import timedelta
from datetime import date
import random
import time

#создаем название файла для сохранения данных о количестве объявлений
CSV = 'avito_counts.csv'
# адрес хостинга
HOST = 'https://www.avito.ru/'

# точный адрес страницы с которой будем парсить(внутренней страницы сайта)
URL = 'https://www.avito.ru/ryazan/kvartiry/prodam/novostroyka-ASgBAQICAUSSA8YQAUDmBxSOUg'

# прописываем заголовки, которые будем отправлять вместе с запросами
HEADERS = {
    'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'
   }

#создаем функцию, которая получает html код страницы и записывает его в переменную r
def get_html(url,params = ''):
    r = requests.get(url,headers=HEADERS,params=params)
    time.sleep(random.randint(1,6))
    return r



# функция получает на вход ход страницы и находит, сколько всего страниц нужно спарсить(пагинация)
def get_pagination(html):
    soup = BeautifulSoup(html.text, features="html.parser")
    page_tags = soup.find_all('span', class_="pagination-item-1WyVp")
    
    #сразу чистим от тегов до чистого текста и в датафрейм
    pages = pd.DataFrame(columns = ['page'])
    for i in range(len(page_tags)):
        pages.loc[i] = page_tags[i].text
    
    #т.к. к нам попадают кроме страниц еще надписи "пред." и "след.", уберем их  и многоточее
    pages = pages.query('page != "← Пред." and page !="След. →" and page != "..."')
    
    # теперь выясняем номер самой большой страницы
    pagination = pages['page'].astype('int').max()
    
    return pagination



# функция получает полный html код страницы и находит в нем содержимое тега span c параметром class_="snippet-link-name"
# в этих ячейках(тегах) хранятся данные о количестве комнат, метраже, и этаже
def get_df(html):
    soup = BeautifulSoup(html.text, features="html.parser")
    cells = soup.find_all('span', class_="title-root-395AQ iva-item-title-1Rmmj title-listRedesign-3RaU2 title-root_maxHeight-3obWc text-text-1PdBw text-size-s-1PUdo text-bold-3R9dt")
    
    
    #сразу чистим от тегов до чистого текста и в датафрейм
    df = pd.DataFrame(columns = ['specifications'])
    for i in range(len(cells)):
        df.loc[i] = cells[i].text
    return df




# функция получает полный html код страницы и находит в нем содержимое тега meta c параметром itemprop="price"
# в этих ячейках(тегах) хранятся данные о цене
def get_prices(html):
    soup = BeautifulSoup(html.text, features="html.parser")
    prices_tags = soup.find_all('span', class_="price-text-1HrJ_ text-text-1PdBw text-size-s-1PUdo")
    
    #теперь очищаем от тегов до чистой цены и сразу в датафрейм
    prices = pd.DataFrame(columns = ['price'])
    for i in range(len(prices_tags)):
        prices.loc[i] = prices_tags[i].text
    prices['price'] = prices['price'].apply(lambda x: re.sub(' ', '',x))
    prices['price'] = prices['price'].apply(lambda x: (re.search('\d+',x)).group(0))
    return prices


# функция получает полный html код страницы и находит в нем содержимое тега span c параметром class_="geo-address-9QndR text-text-1PdBw text-size-s-1PUdo"
# в этих ячейках(тегах) хранятся данные об адресах
def get_addresses(html):
    soup = BeautifulSoup(html.text, features="html.parser")
    streets_tags = soup.find_all('span', class_="geo-address-9QndR text-text-1PdBw text-size-s-1PUdo")
    
    #сразу чистим от тегов до чистого текста и в датафрейм
    addresses = pd.DataFrame(columns = ['address'])
    for i in range(len(streets_tags)):
        addresses.loc[i] = streets_tags[i].text
    return addresses



# функция получает полный html код страницы и находит в нем содержимое тега div c параметром class="snippet-date-info"
# в этих ячейках(тегах) хранятся данные о дате подачи/обновления объявления
def get_dates(html):
    soup = BeautifulSoup(html.text, features="html.parser")
    date_tags = soup.find_all('div', class_="date-text-2jSvU text-text-1PdBw text-size-s-1PUdo text-color-noaccent-bzEdI")
    
    #теперь очищаем от тегов до чистой цены и сразу в датафрейм
    dates = pd.DataFrame(columns = ['date'])
    for i in range(len(date_tags)):
        dates.loc[i] = date_tags[i].text
    return dates

# функция парсер собирает все предыдущие действия в единый порядок, запуск этой функции и есть запуск программы
def parser ():
    
    #парсим основную страницу чтобы узнать, сколько всего страниц
    html = get_html(URL)
    print('Статус парсинга первой страницы:',html.status_code)
    pagination = get_pagination(html)
    print('Pages count:',pagination)
    
    
    #если потучилось добыть код страницы, то запускаем цикл постраничного парсинга
    if html.status_code == 200:
        avito_counts = pd.DataFrame(columns = ['specifications', 'price', 'address', 'date', 'parsing_dt'])
        for page in range(1, pagination+1):
            print('Parse page{}'.format(page))
            
            #получаем код n-ной страницы
            html = get_html(URL, params={'cd':1, 'p':page})
            
            #собираем все данные в колонки датафреймов
            df = get_df(html).reset_index()
            prices = get_prices(html).reset_index()
            addresses = get_addresses(html).reset_index()
            dates = get_dates(html).reset_index()
            #Важно! Часть дат не парсится. Это происходит потому, что в VIP объявлениях нет точных дат.
            # И это очень удачно, т.к. VIP объявления - дублирующие. Для анализа их нужно будет убрать.
            # Отсутствие даты - явный идентификатор таких объявлений, по которому их будет очень удобно отследить и удалить.
            
            
            
            
            #объединяем все колонки в один датафрейм
            data = df.merge(prices, on='index').merge(addresses, on='index').merge(dates, on='index')
            
            #Чтобы не увеличивать объемы данных, сразу зачистим от дублей, которыми являются ВИП объявления. 
            # Метод duplicated() применять нельзя, т.к. объявление иногда расположено уже после своего  ВИП дублера, и тогда будет
            # удален экземпляр с датой, а ВИП объявление останется, и в базе будет отсутствовать дата.
            # По этому необходимо просто сбросить строки с пустыми датами.
            data = data[data['date'] != ''].reset_index(drop=True)
            
            
            # столбец индекс тоже больше не нужен
            del data['index']



            # для будущих изысканий добавим дату парсинга
            data['parsing_dt'] = datetime.datetime.now()
            
            
            avito_counts = pd.concat([avito_counts,data]).reset_index(drop=True)
            
            print('Parsing successful')
            
    else:
        print('parsing_error')
        print(html.status_code)
    return avito_counts

avito_counts = parser()

# это для логов
print(avito_counts.info())

# последний штрих. записываем в csv c текущей датой

avito_counts.to_csv('AviroParserPrima{}.csv'.format(datetime.datetime.today().strftime('%Y-%m-%d')), mode='w', index=False, sep=';', encoding='utf8')
   
print('csv_saving_done:'.format(datetime.datetime.today().strftime('%Y-%m-%d')))
