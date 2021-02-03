#!/usr/bin/python
# -*- coding: utf-8 -*-

import dash
import dash_core_components as dcc
import dash_html_components as html
import datetime
import time
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import threading


        
# задаём лейаут (макет)
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(children=[  

    # формируем заголовок
    html.Div(style={'color':'white','background':'#4671D5', 'textAlign': 'center'}, children=[
        html.H1(children = 'Анализ предложения новостроек Рязани по данным объявлений Avito.ru')
        ]),

    # имя автора и дата последнего обновления
    html.H4(style={'marginLeft': 20},children = 'Автор: Лев Васильев'),
    html.Div( id='date'),

    #Создаем первый контейнер графиков
    html.Div(children=[

        # элемент управления
        html.Div(style={'color':'white','background':'#4671D5', 'textAlign': 'center'},children=[
            html.H4(children = 'Какие квартиры Вас интересуют?'),
            dcc.Checklist( options = [{'label': '1-к квартиры(включая студии)', 'value': '1'}, 
                          {'label': '2-к квартиры', 'value': '2'}, 
                          {'label': '3-к квартиры', 'value': '3'}, 
                          {'label': '4-к квартиры', 'value': '4'}], 
               value = ['1', '2', '3', '4'],
               labelStyle={'display': 'inline-block'},
               id = 'price_range_checklist'
                       ),
            ]),
        #азвание графика
        html.H4(style={'marginLeft': 70},children = 'Распределение предложений на новостройки по стоимости:'),

        # график 
        dcc.Graph( id = 'price_range')
        ]),
    #Создаем второй контейнер графиков
    html.Div(children=[

        #название графика
        html.H4(style={'marginLeft': 70},children = 'Распределение предложений на новостройки по стоимости квадратного метра:'),

        # график 
        dcc.Graph( id = 'price_m2_range')
        ]),
    
    #Создаем третий контейнер графиков
    html.Div(children=[
        html.Div( children=[
            #название графика
            html.H4(style={'marginLeft': 70},children = 'Доля квартир с разным количеством комнат:'),

            # график 1 
            dcc.Graph( id = 'pie_rooms')
            ],className = 'five columns'),

        html.Div( children=[
            #название графика
            html.H4(style={'marginLeft': 70},children = 'Распределение квартир по метражу:'),

            # график 2 
            dcc.Graph( id = 'dist_m2')
            ],className = 'seven columns'),
        ],className = 'row'),

    # заголовок раздела динамических показателей
    html.Div(style={'color':'white','background':'#4671D5', 'textAlign': 'center'}, children=[
        html.H4(children = 'Динамические показатели с начала наблюдения по текущую дату')
        ]),
    html.Div(children=[
         html.Div( children=[
             html.H4(children = 'Медианная стоимость квартир'),
             dcc.Graph( id = 'price_dinamic')],className = 'six columns'),
             html.Div( children=[
                 html.H4(children = 'Медианная стоимость квадратного метра'),
                 dcc.Graph( id = 'price_m2_dinamic')],className = 'six columns'),
         
        ],className = 'row'),
    html.Div( children=[
                 html.H4(children = 'Количество предложений квартир'),
                 dcc.Graph( id = 'offers_dinamic'),
             ]),
])
    

# описываем логику дашборда

@app.callback(
    [Output('price_range', 'figure'),
     Output('price_m2_range', 'figure'),
     Output('dist_m2', 'figure'),
     Output('date','children'),
     Output('pie_rooms','figure'),
     Output('price_dinamic','figure'),
     Output('price_m2_dinamic','figure'),
     Output('offers_dinamic','figure'),
    ],
    [Input('price_range_checklist', 'value'),
    ])
def update_figures(selected_rooms):
    # Читаем данные, которые понадобятся для борда
    current_data = pd.read_csv('AviroParserPrimaTransformed2020-11-30.csv', sep=';')
    # настраиваем формат времени
    current_data['parsing_dt'] =pd.to_datetime(current_data['parsing_dt'],format='%Y-%m-%d %H:%M:%S')
    # удаляем неправдоподобные значения
    current_data = current_data.query('price > 500000 and rooms <10') 
    last_data = pd.read_csv('AviroAggregated.csv', sep=';')

    # фильтруем данные с учетом выбранных параметров
    filtered_current_data = current_data.query('rooms in @selected_rooms')
  
    # формируем графики для отрисовки с учётом фильтров
    price_range = [go.Histogram(x = filtered_current_data['price'], xbins=dict(size=100000))]
    price_m2_range = [go.Histogram(x = filtered_current_data['price_m2'], xbins=dict(size=1000))]
    dist_m2 = [go.Histogram(x = filtered_current_data['m2'], xbins=dict(size=5))]
    pie_rooms = [go.Pie(labels = current_data['rooms'], values = current_data['rooms'], name = 'pie')]
    price_dinamic = [go.Scatter(x = last_data['date'], 
                                       y = last_data['price'], 
                                       mode = 'lines', 
                                       name = 'Общая'),
                            go.Scatter(x = last_data['date'], 
                                       y = last_data['1-room_price'], 
                                       mode = 'lines', 
                                       name = '1к квартир'),
                            go.Scatter(x = last_data['date'], 
                                       y = last_data['2-room_price'], 
                                       mode = 'lines', 
                                       name = '2к квартир'),
                            go.Scatter(x = last_data['date'], 
                                       y = last_data['3-room_price'], 
                                       mode = 'lines', 
                                       name = '3к квартир'),
                            go.Scatter(x = last_data['date'], 
                                       y = last_data['>=4-room_price'], 
                                       mode = 'lines', 
                                       name = '4к и более'),
                            ]
    price_m2_dinamic = [go.Scatter(x = last_data['date'], 
                                       y = last_data['price_m2'], 
                                       mode = 'lines', 
                                       name = 'Общая'),
                            go.Scatter(x = last_data['date'], 
                                       y = last_data['1-room_price_m2'], 
                                       mode = 'lines', 
                                       name = '1к квартир'),
                            go.Scatter(x = last_data['date'], 
                                       y = last_data['2-room_price_m2'], 
                                       mode = 'lines', 
                                       name = '2к квартир'),
                            go.Scatter(x = last_data['date'], 
                                       y = last_data['3-room_price_m2'], 
                                       mode = 'lines', 
                                       name = '3к квартир'),
                            go.Scatter(x = last_data['date'], 
                                       y = last_data['>=4-room_price_m2'], 
                                       mode = 'lines', 
                                       name = '4к и более'),
                            ]
    offers_dinamic = [go.Scatter(x = last_data['date'], 
                                       y = last_data['offers_counts'], 
                                       mode = 'lines', 
                                       name = 'Всего предложений'),
                            go.Scatter(x = last_data['date'], 
                                       y = last_data['1r_offers_counts'], 
                                       mode = 'lines', 
                                       name = '1к квартир'),
                            go.Scatter(x = last_data['date'], 
                                       y = last_data['2r_offers_counts'], 
                                       mode = 'lines', 
                                       name = '2к квартир'),
                            go.Scatter(x = last_data['date'], 
                                       y = last_data['3r_offers_counts'], 
                                       mode = 'lines', 
                                       name = '3к квартир'),
                            go.Scatter(x = last_data['date'], 
                                       y = last_data['>=4r_offers_counts'], 
                                       mode = 'lines', 
                                       name = '4к и более'),
                            ]
    # формируем результат для отображения
    
    return (
            {
                'data': price_range,
                'layout': go.Layout(xaxis = {'title': 'Стоимость квартиры (млн руб.)'},
                                    yaxis = {'title': 'Количество предложений (шт.)'},
                                    bargap = 0.05)
             },
            {
                'data': price_m2_range,
                'layout': go.Layout(xaxis = {'title': 'Стоимость за метр квадратный (тыс. руб.)'},
                                    yaxis = {'title': 'Количество предложений (шт.)'},
                                    bargap = 0.05)
             },
            {
                'data': dist_m2,
                'layout': go.Layout(xaxis = {'title': 'Площадь квартиры (м²)'},
                                    yaxis = {'title': 'Количество предложений (шт.)'},
                                    bargap = 0.05)
             },
            'Дата последнего обновления: {}'.format((current_data['parsing_dt'].max()).strftime(format='%d-%m-%Y')),

            {   'data': pie_rooms,
                'layout': go.Layout()
            },
            {   'data': price_dinamic,
                'layout': go.Layout(xaxis = {'title': 'Дата'}, yaxis = {'title': 'Стоимость квартир (млн руб.)'})
            },
            {   'data': price_m2_dinamic,
                'layout': go.Layout(xaxis = {'title': 'Дата'}, yaxis = {'title': 'Стоимость квадратного метра (тыс. руб.)'})
            },
            {   'data': offers_dinamic,
                'layout': go.Layout(xaxis = {'title': 'Дата'}, yaxis = {'title': 'Количество предложений квартир (шт.)'})
            },
            
  )

    
if __name__ == '__main__':
    app.run_server(debug = True, host = '0.0.0.0')
        
   
