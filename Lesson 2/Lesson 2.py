# Вариант 1

# Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы) с сайтов
# Superjob и HH. Приложение должно анализировать несколько страниц сайта (также вводим через input или аргументы).
# Получившийся список должен содержать в себе минимум: Наименование вакансии. Предлагаемую зарплату (отдельно
# минимальную и максимальную). Ссылку на саму вакансию. Сайт, откуда собрана вакансия. ### По желанию можно добавить
# ещё параметры вакансии (например, работодателя и расположение). Структура должна быть одинаковая для вакансий с
# обоих сайтов. Общий результат можно вывести с помощью dataFrame через pandas.

import json
import time
from pprint import pprint
import pickle
import requests
from bs4 import BeautifulSoup as bs


def save_pickle(obj, path):
    with open(path, 'wb') as write_file:
        pickle.dump(obj, write_file)


def load_pickle(path):
    with open(path, 'rb') as read_file:
        return pickle.load(read_file)


def get(url, headers, params, proxies):
    req = requests.get(url, headers=headers, params=params, proxies=proxies)
    return req


# vacancy = input('Введите текст или слово для поиска вакансии: ')
#
# # https://hh.ru/search/vacancy?L_is_autosearch=false&clusters=true&enable_snippets=true&text=python&page=1
#
# url = "https://hh.ru/search/vacancy"
#
# params = {
#     'L_is_autosearch': 'false',
#     'clusters': 'true',
#     'enable_snippets': 'true',
#     'text': vacancy,
#     # 'page':
# }
# headers = {
#     'User-Agent': "Mozilla/5.0 (Windows; U; Windows NT 5.1; ru-RU) AppleWebKit/533.18.1 (KHTML, like Gecko) "
#                   "Version/5.0.2 Safari/533.18.5 "
# }
# proxies = {
#     'http': 'http://3.88.169.225:80',
#     # 'https': 'https://165.227.223.19:3128',
# }
#
# req = get(url, headers, params, proxies)
#
# path = "hh.rsp"
# save_pickle(req, path)

path = "hh.rsp"
req = load_pickle(path)
soup = bs(req.text, 'html.parser')
# print(soup)

# вакансия
vacancy_info = soup.find(attrs={"class": "vacancy-serp-item",
                                "data-qa": "vacancy-serp__vacancy"
                                }#,
                             #limit=2
                             )

# print(vacancy_info)
# print(vacancy_info.a['href'])

vacancies = []

for i_tag in vacancy_info:
    info = {}
    # название вакансии
    vacancy_name = i_tag.find(attrs={"class": "bloko-link HH-LinkModifier HH-VacancyActivityAnalytics-Vacancy"}).text
    # Ссылка на саму вакансию
    href = i_tag.find(attrs={"class": "g-user-content"}).a['href']
    # Сайт, откуда собрана вакансия
    resource = 'https://hh.ru/'
    info['vacancy_name'] = vacancy_name
    info['href'] = href
    info['resource'] = resource
    try:
        # Предлагаемая зп
        zp = i_tag.find(attrs={"data-qa": "vacancy-serp__vacancy-compensation"}).text
        info['zp'] = zp
    except Exception:
        pass

    vacancies.append(info)

pprint(vacancies)
print(len(info))
print(len(vacancies))
