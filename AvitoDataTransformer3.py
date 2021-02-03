#!/usr/bin/env python
# coding: utf-8

# In[127]:


import pandas as pd
import re
import datetime

# закачиваем таблицу с черновыми данными парсинга за текущую дату
df = pd.read_csv('AviroParserPrima{}.csv'.format(datetime.datetime.today().strftime('%Y-%m-%d')), sep=';')
df.head()


# выделяем количество квадратных метров в отдельный столбец с помощью регулярного выражения
df['m2'] = df['specifications'].apply(lambda x: re.sub(' ', '', re.sub(' м²', '', (re.split(',',x))[1])))
df['m2'] = df['m2'].astype('float')

# выделяем количество комнат в отдельный столбец с помощью регулярного выражения
df['rooms'] = df['specifications'].apply(lambda x: (re.search('\d+',x)).group(0))
df['rooms'] = df['rooms'].astype('int')

# баг. выражение выше читает метраж студий, как количество комнат.
# выход, назначаем все студии(квартиры с метражем менее 35м2 и кол-вом комнат более 15)однокомнатными
# люди чаще указывают студии как 1-к квартиры, так что разделить все равно не удастся
for i in range(len(df)):
    if df.loc[i,'rooms']>15 and df.loc[i,'m2']<35:
        df.loc[i,'rooms'] = 1

# выделяем этаж в отдельный столбец с помощью регулярного выражения
df['floor'] = df['specifications'].apply(lambda x:re.sub('/.+','',re.sub(' эт.\n', '',(re.split(',',x))[2])))

# выделяем кол-во этажей в доме в отдельный столбец с помощью регулярного выражения
df['from_floors'] = df['specifications'].apply(lambda x:re.sub('.+/','',re.sub(' эт.\n', '',(re.split(',',x))[2])))

# столбец 'specifications' больше не нужен
#del df['specifications']

# из-за текстового, да еще и русского формата даты, преобразовать строку в тип datetime напрямую не получится
# по этому, сначала делаем словарь, где каждому кирилическому месяцу соответствует его номер
#months =(
#       {'января':'1','февраля':'2','марта':'3','апреля':'4','мая':'5',
#         'июня':'6','июля':'7','августа':'8','сентября':'9','октября':'10',
#        'ноября':'11','декабря':'12'})

# теперь, при помощи регулярного выражения заменяем названия месяцев на их номер и попутно добавляем текущий год 
#(Важно! добавляем текущий год потому, что преобразование подразумевается в день парсинга. Если модуль будет использоваться на старых данных, нужно будет что то менять.)
#df['dt'] = df['date'].apply(lambda x:re.sub('[а-я]+',(months[re.search('[а-я]+',x).group(0)])+' '+datetime.datetime.now().strftime('%Y'),x))

# и теперь переводим в формат датывремени
#df['dt'] = pd.to_datetime(df['dt'],format='%d %m %Y %H:%M')

# переведем метры в числовой формат и рассчитаем цену квадратного метра для каждого объекта
df['m2'] = df['m2'].astype('float64')
df['price_m2'] = df['price']/df['m2']
df['price_m2'] = df['price_m2'].astype('int')

# скачиваем данные об улицах Рязани и и паттернах, по которым, их можно вычислить(Пришлось сделать такой список вручную)
ruazan_addresses = pd.read_csv('addresses_data.csv',sep=';')

# создаем столбец улицы и путем перебора в цикле заполняем его паттернами, которые удастся найти в df['address']
df['streets']='Unknown'
for i in range(0,len(ruazan_addresses)):
    for x in range(0,len(df)):
        try:
            df.loc[x,'streets'] = (re.search(ruazan_addresses.loc[i,'short_names'], df.loc[x,'address'])).group(0)
        except Exception:
            R=1 #это действие пустышка, т.е. , если паттерн не найден, в ячейке df.loc[x,'streets'] ничего не произойдет, останется изначальное значение Unknown 
            
# т.к. некоторые улицы города дублируются в разных локациях, то создадим список доп локаций, где это возможно и передадим в датафрейм
districs = ['Дягилево',
'Соколовка',
'Канищево',
'Шереметьево-Песочня',
'Недостоево',
'Семчино',
'Заборье',
]
districts_data = pd.DataFrame(districs, columns = ['district'])


# ищем паттерны доп локаций и добавляем к паттернам улиц
# такие составные паттерны сами по себе будут соответствовать улицам с пометками доп локаций в таблице ruazan_addresses
for x in range(0,len(df)):
    for i in range(0,len(districts_data)):
        try:
            df.loc[x,'streets'] = (
                df.loc[x,'streets']+' '+'('+' '+
                ((re.search(districts_data.loc[i,'district'], df.loc[x,'address'])).group(0))
                +')'
            )
        except Exception:
            R=1 # действие пустышка
            

# теперь, перебираем в df['streets'] все паттерны, и назначаем им соответствующие улицы из ruazan_addresses            
for i in range(len(df)):
    for x in range(len(ruazan_addresses)):
        if df.loc[i, 'streets'] == ruazan_addresses.loc[x, 'short_names']:
            df.loc[i, 'streets'] = ruazan_addresses.loc[x, 'street_names']
        else:
            R=1

            
 # последний штрих. записываем в csv c текущей датой

df.to_csv('AviroParserPrimaTransformed{}.csv'.format(datetime.datetime.today().strftime('%Y-%m-%d')), mode='w', index=False, sep=';', encoding='utf8')

print('csv_savig_done:'.format(datetime.datetime.today().strftime('%Y-%m-%d')))           

