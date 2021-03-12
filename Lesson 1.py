# Задание 1


# import requests
import json
from pprint import pprint
# pip install fake-useragent
from fake_useragent import UserAgent


ua = UserAgent()

# Имя пользователя
username = 'naumchenkomk'

url = f"https://api.github.com/users/{username}/repos"
headers = {
    "User-Agent": ua.random
}
r = requests.get(url, headers=headers)
# делаем запрос и возвращаем json

data = (requests.get(url).json())
pprint(data)

with open('response.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, indent=2, ensure_ascii=False)


# Задание 2





