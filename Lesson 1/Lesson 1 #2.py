# Задание 2
# Изучить список открытых API. Найти среди них любое, требующее авторизацию (любого типа). Выполнить запросы к нему,
# пройдя авторизацию. Ответ сервера записать в файл.
import requests
import json
from pprint import pprint
from fake_useragent import UserAgent


ua = UserAgent()
lat = 55.76
lng = 37.62
dt = '2021-03-12T19:16:28.159Z'
API_Key = 'aa1aac844caf77954a0724448632584b'

url2 = f"https://api.openuv.io/api/v1/uv?lat={lat}&lng={lng}&dt={dt}"

headers2 = {
    "User-Agent": ua.random,
    'x-access-token': API_Key
}
req2 = requests.get(url2, headers=headers2)
# делаем запрос и возвращаем json
data2 = (req2.json())
pprint(data2)

with open('response #2.json', 'w', encoding='utf-8') as file:
    json.dump(data2, file, indent=2, ensure_ascii=False)