# Дашборд рынка новостроек Рязани на основе парсинга данных с Авито
## Пример автоматизации аналитики на основе открытых данных. (Проект заморожен)
### Основные библиотеки:
1. Парсер: requests, BeautifulSoup, Mystem, pandas, datetime
2. Обработка и аггрегация данных: pandas, re, datetime
3. Дашборд: pandas, dash, datetime, plotly.graph_obj

### Описание
Проект состоит из нескольких этапов, где каждый этап осуществляется отдельным скриптом написанным на Python:
1. Сбор открытых данных с сервиса Авито при помощи скрипта AvitoParser5.py(в настоящий момент скрипт не сработает в связи с изменением кода страницы Авито). Результатом срабатывания скрипта является файл с необработанными данными объявлений на текущую дату(Пример файла - AviroParserPrima2020-11-30.csv).
2. Предобработка. Приведение полученных данных в пригодный для аналитики вид. Осуществляется скриптом AvitoDataTransformer3.py. Результат - файл с готовыми для аналитики данными. (Пример файла - AvitoParserPrimaTransformed2020-11-30.csv)
3. Аггрегация данных. Формирование дополнительных аггрегированных данных для контроля динамики процессов во времени. Скрипт - AvitoAggregator.py. Эти данные записываются в отдельный файл. (Пример файла - AvitoAggregated.csv)
4. Формирование дашборда. Скрипт AvitoDash5.py на основе библиотеки Dash.

### Запуск
Хотя в настоящий момент проект заморожен, возможно посмотреть как выглядел дашборд на последнюю рабочую дату. Для этого потребуется:
1. скачать на локальный компьютер в одну папку:
 - скрипт "AvitoDash5.py"
 - файл данных "AvitoParserPrimaTransformed2020-11-30.csv"
 - файл данных "AvitoAggregated.csv"
2. Запустить скрипт при помощи любого интерпретатора Python
3. Открыть браузер и ввести в адресной строке http://127.0.0.1:8050/

### Примеры визуализации:
![1.](https://github.com/GitPilgrim/Dashboard_Avito_Ruazan_realty/raw/main/Screenshot_m2.jpg)
![2.](https://github.com/GitPilgrim/Dashboard_Avito_Ruazan_realty/raw/main/Screenshot_median.jpg)
![3.](https://github.com/GitPilgrim/Dashboard_Avito_Ruazan_realty/raw/main/Screenshot_other.jpg)
![4.](https://github.com/GitPilgrim/Dashboard_Avito_Ruazan_realty/raw/main/Screenshot_price.jpg)
























