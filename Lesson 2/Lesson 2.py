# Вариант 1

# Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы) с сайтов
# Superjob и HH. Приложение должно анализировать несколько страниц сайта (также вводим через input или аргументы).
# Получившийся список должен содержать в себе минимум: Наименование вакансии. Предлагаемую зарплату (отдельно
# минимальную и максимальную). Ссылку на саму вакансию. Сайт, откуда собрана вакансия. ### По желанию можно добавить
# ещё параметры вакансии (например, работодателя и расположение). Структура должна быть одинаковая для вакансий с
# обоих сайтов. Общий результат можно вывести с помощью dataFrame через pandas.

import json
import time
import random
from pprint import pprint
import pickle
import requests
from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent
u = UserAgent().random


# Сохранение результата запроса к HH в файл (0) - pickle

def save_pickle(obj, path):
    with open(path, 'ab+') as add_file:
        pickle.dump(obj, add_file)


def load_pickle(path):
    with open(path, 'rb') as read_file:
        return pickle.load(read_file)


def get(url, headers, params, proxies):
    req = requests.get(url, headers=headers, params=params, proxies=proxies)
    return req


# Сохранение результата запроса к HH в файл (1) - проверка на то, что страница является последней

def is_last_page(request):
    soup_incr = bs(request.text, 'html.parser')
    is_end = soup_incr.find(attrs={"class": "bloko-button HH-Pager-Controls-Next HH-Pager-Control"}) is None
    return is_end


# Сохранение результата запроса к HH в файл (2)

def hh_request(word, page_nbr, f_name):
    for i in range(10):
        try:
            path_inc = f"{f_name}_inc.rsp"
            # очищаем файл для записи одной страницы
            f = open(path_inc, 'w')
            f.close()
            # Браузер
            ua = UserAgent().random

            url = "https://hh.ru/search/vacancy"
            params = {
                'L_is_autosearch': 'false',
                'clusters': 'true',
                'enable_snippets': 'true',
                'text': word,
                'page': page_nbr
            }
            headers = {
                'User-Agent': ua
            }
            proxies = {
                'http': 'http://3.88.169.225:80',
                # 'https': 'https://165.227.223.19:3128',
            }
            answ = get(url, headers, params, proxies)
            answ.encoding = 'utf-8'
            print('Статус запроса к текущей странице:', answ)

            if answ.status_code != 200:
                raise Exception

            save_pickle(answ, path_inc)
            save_pickle(answ, f"{f_name}.rsp")

            return answ
        except Exception as e:
            if answ.status_code == 404:
                print('Задана несуществующая страница. Попробуйте еще раз.')
                return answ.status_code
            else:
                print(e, 'попытка №', i)
                time.sleep(0.5 + random.random())


# парсинг файла с результатом запроса к HH (1) - зарплата

def zp_pars(sum):
    sum = sum.replace('\xa0', '')
    sum = sum.replace('\u202f', '')
    if sum.find('от ') != -1:
        sum_min = int(sum[sum.find(' ') + 1:sum.rfind(' ')])
        sum_max = None
    elif sum.find('до') != -1:
        sum_min = None
        sum_max = int(sum[sum.find(' ') + 1:sum.rfind(' ')])
    else:
        sum_min = sum[0:sum.find('-')]
        sum_max = sum[sum.find('-') + 1:sum.rfind(' ')]
    curr = sum[sum.rfind(' ') + 1:len(sum)]
    return [sum_min, sum_max, curr]


# парсинг файла с результатом запроса к HH (2) - Парсинг одной страницы HH (одного документа HTML)

def hh_parser(f_name_in, f_name_out):
    req = load_pickle(f"{f_name_in}_inc.rsp")
    soup = bs(req.text, 'html.parser')

    # вакансия
    vacancy_info = soup.find_all(attrs={"class": "vacancy-serp-item"})
    hh_vacancies = []

    for i_tag in vacancy_info:
        info = {}
        # название вакансии
        vacancy_name = i_tag.find(attrs={"data-qa": "vacancy-serp__vacancy-title"}).text.replace('\xa0', '')
        # Ссылка на саму вакансию
        link = i_tag.find(attrs={"class": "resume-search-item__name"}).a['href']
        # Порядковый номер вакансии в результате запроса
        poz = i_tag.find(attrs={"class": "resume-search-item__name"}).a['data-position']
        # Сайт, откуда собрана вакансия
        resource = 'https://hh.ru/'

        info['vacancy_name'] = vacancy_name
        info['link'] = link
        info['poz'] = poz
        info['resource'] = resource

        # vacancies.append(info)
        try:
            # Предлагаемая зп
            zp = i_tag.find(attrs={"data-qa": "vacancy-serp__vacancy-compensation"}).text
            zp_min = zp_pars(zp)[0]
            zp_max = zp_pars(zp)[1]
            zp_curr = zp_pars(zp)[2]
            info['zp_min'] = zp_min
            info['zp_max'] = zp_max
            info['zp_curr'] = zp_curr
        except AttributeError:
            pass

        hh_vacancies.append(info)

    with open(f"{f_name_out}_inc.json", "w+") as f:
        json.dump(hh_vacancies, f, indent=2) #, ensure_ascii=False)

    return hh_vacancies


# парсинг файла с результатом запроса к HH (3) - сохранение в json-файл результата работы парсера

def json_add_to_file(f_name, page):
    with open(f"{f_name}_inc.json", "r") as f:
        to_file = json.load(f)
        file = to_file

    if page == 0:
        with open(f"{f_name}.json", "w+") as f:
            json.dump(file, f, indent=2) #, ensure_ascii=False)
    else:
        with open(f"{f_name}.json", "r") as f:
            to_file_total = json.load(f)
            file = to_file_total + to_file
        with open(f"{f_name}.json", "w+") as f:
            json.dump(file, f, indent=2) #, ensure_ascii=False)


# парсинг файла с результатом запроса к HH (4) - запуск постраничного парсинга и вывод результата пользователю

def hh_parser_result(f_name_req, f_name_out):
    # word_vacancy = 'python'
    word_vacancy = input('Введите слово или фразу для поиска вакансий: ')
    # pages_nbr = 2
    pages_nbr = int(input('Сколько страниц хотите просмотреть? '))
    page_start = int(input('С какой страницы хотите начать просмотр? '))
    i = 0
    while i < pages_nbr:
        page_curr = page_start - 1 + i
        print("Страница", page_curr + 1)
        hh_request_res = hh_request(word_vacancy, page_curr, f_name_req)
        if hh_request_res == 404:
            return False
        hh_parser_res = hh_parser(f_name_req, f_name_out)
        json_add_to_file(f_name_out, i)
        if is_last_page(hh_request_res):  # выход, если последняя страница
            print('Последняя страница была обработана')
            break
        else:
            print(f'Количество вакансий на странице {page_curr + 1}:', len(hh_parser_res))
        i = i + 1

    with open(f"{f_name_out}.json", "r") as f:
        hh_vacancies_full = json.load(f)
        print()
        print('Количество вакансий, суммарное:', len(hh_vacancies_full))
        vacancies_nbr = int(input('Сколько вакансий показать? '))

        print('Вакансии:')
        pprint(hh_vacancies_full[0:vacancies_nbr])


# Пред обработка (1) - задание названия файла для сохранения результатов запроса и парсинга

f_name_req = "hh_vacancies_search_result"
f_name_out = 'hh_vacancies_parsed'

# Пред обработка (2) - создание файла или очистка, если он уже существует

# очищаем полный файл ответа от HH
f = open(f"{f_name_req}.rsp", 'w+')
f.close()

# очищаем полный файл json
f = open(f"{f_name_out}.json", 'w+')
f.close()

# Запуск программы парсинга HH
hh_parser_result(f_name_req, f_name_out)


######### TODO PANDAS
