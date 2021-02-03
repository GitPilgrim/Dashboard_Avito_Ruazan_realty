#!/usr/bin/env python
# coding: utf-8



import pandas as pd
import datetime



# закачиваем таблицу с черновыми данными парсинга за текущую дату
df = pd.read_csv('AviroParserPrimaTransformed{}.csv'.format(datetime.datetime.today().strftime('%Y-%m-%d')), sep=';')




#df['dt'] = pd.to_datetime(df['dt'],format='%Y %m %d %H:%M')
df['parsing_dt'] = pd.to_datetime(df['parsing_dt'],format='%Y %m %d %H:%M')

aggregated_data = pd.DataFrame(columns = ['date', 'price_m2','1-room_price_m2','2-room_price_m2','3-room_price_m2','>=4-room_price_m2'])

aggregated_data.loc[1,'date'] = df['parsing_dt'].max().strftime(format='%Y-%m-%d %H:%M')

aggregated_data.loc[1,'price_m2'] = df['price_m2'].median()

aggregated_data.loc[1,'price'] = df['price'].median()

aggregated_data.loc[1,'1-room_price'] = df.query('rooms == 1')['price'].median()

aggregated_data.loc[1,'2-room_price'] = df.query('rooms == 2')['price'].median()

aggregated_data.loc[1,'3-room_price'] = df.query('rooms == 3')['price'].median()

aggregated_data.loc[1,'>=4-room_price'] = df.query('rooms >= 4')['price'].median()

aggregated_data.loc[1,'price_m2'] = df['price_m2'].median()

aggregated_data.loc[1,'1-room_price_m2'] = df.query('rooms == 1')['price_m2'].median()

aggregated_data.loc[1,'2-room_price_m2'] = df.query('rooms == 2')['price_m2'].median()

aggregated_data.loc[1,'3-room_price_m2'] = df.query('rooms == 3')['price_m2'].median()

aggregated_data.loc[1,'>=4-room_price_m2'] = df.query('rooms == 4')['price_m2'].median()

aggregated_data.loc[1,'offers_counts'] = df.shape[0]
aggregated_data.loc[1,'1r_offers_counts'] = df.query('rooms == 1').shape[0]
aggregated_data.loc[1,'2r_offers_counts'] = df.query('rooms == 2').shape[0]
aggregated_data.loc[1,'3r_offers_counts'] = df.query('rooms == 3').shape[0]
aggregated_data.loc[1,'>=4r_offers_counts'] = df.query('rooms >= 4').shape[0]

columns = ['price_m2',
                  '1-room_price_m2',
                  '2-room_price_m2',
                  '3-room_price_m2',
                  '>=4-room_price_m2',
                  'price',
                  '1-room_price',
                  '2-room_price',
                  '3-room_price',
                  '>=4-room_price']

for column in columns:
    aggregated_data[column] = aggregated_data[column].astype('int')   





# последний штрих. Дописываем в существующий csv

aggregated_data.to_csv('AviroAggregated.csv', mode='a',header=False, index=False, sep=';', encoding='utf8')

print('csv_saving_done:'.format(datetime.datetime.today().strftime('%Y-%m-%d')))






