################################
# Lesson 1

# pip install requests
# pip install -U python-dotenv
# import requests

# req = requests.put("http://httpbin.org/put")
# req = requests.delete("http://httpbin.org/delete")
# req = requests.head("http://httpbin.org/get")
# req = requests.options("http://httpbin.org/get")
# Результатом запроса будет объект response
# print(type(req))
# print(req.json())

# headers = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
#            'Authorization': 'Basic cG9zdG1hbjpwYXNzd29yZA=='}
#
# req = requests.get("https://yandex.ru", headers=headers)
# print('Заголовки: \n', req.headers)
# print('Ответ (содержимое страницы): \n', req.text)

# -------------------- Пример работы с API
#
# import requests
# import json
#
# appid = 'b6907d289e10d714a6e88b30761fae22'
# service = 'https://samples.openweathermap.org/data/2.5/weather'
# req = requests.get(f'{service}?q=&appid={appid}')
# # print(req.text)
# data = json.loads(req.text)
# print(f"В городе {data['name']} {data['main']['temp']} градусов по Кельвину")

################################

# Lesson 2 Урок 2. Парсинг данных_ Парсинг HTML. Beautiful Soup

# pip install bs4
# pip install lxml
#
# from bs4 import BeautifulSoup         #Для обработки HTML
# from bs4 import BeautifulStoneSoup    #Для обработки XML
# import bs4                            #Для обработки и того и другого
# <html>
#     <head>
#         <title>
#             Page title
#         </title>
#     </head>
#     <body>
#         <p id="firstpara" align="center">
#             This is paragraph <b>one</b>.
#         </p>
#         <p id="secondpara" align="blah">
#             This is paragraph <b>two</b>.
#         </p>
#     </body>
# </html>
#
# from bs4 import BeautifulSoup as bs
# import requests
# response = requests.get('http://example.com').text
# print(response)
#
# soup = bs(response, 'lxml') #получаем экземпляр класса bs
# print(soup)

# -------------------- Создание файла

with open('file_name', 'wb') as write_file:
    pickle.dump(obj, write_file)



