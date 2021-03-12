# Задание 1
# Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя,
# сохранить JSON-вывод в файле *.json.

import requests
import json
from pprint import pprint
from fake_useragent import UserAgent


ua = UserAgent()

# Имя пользователя
username = 'naumchenkomk'

# сайт
url = f"https://api.github.com/users/{username}/repos"
headers = {
    "User-Agent": ua.random
}
req = requests.get(url, headers=headers)
# делаем запрос и возвращаем json

data = (req.json())
pprint(data)

with open('response #1.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, indent=2, ensure_ascii=False)







