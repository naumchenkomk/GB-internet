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
from fake_useragent import UserAgent
u = UserAgent()


def save_pickle(obj, path):
    with open(path, 'ab+') as add_file:
        pickle.dump(obj, add_file)


def load_pickle(path):
    with open(path, 'rb') as read_file:
        return pickle.load(read_file)


def get(url, headers, params, proxies):
    req = requests.get(url, headers=headers, params=params, proxies=proxies)
    return req


def zp_pars(sum):
    sum = sum.replace('\xa0', '')
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


def next_page(request):
    soup_incr = bs(request.text, 'html.parser')
    is_end = soup_incr.find(attrs={"class": "bloko-button HH-Pager-Controls-Next HH-Pager-Control"}) is None
    return is_end


# vacancy = input('Введите текст или слово для поиска вакансии: ')

vacancy = 'python'
# https://hh.ru/search/vacancy?L_is_autosearch=false&clusters=true&enable_snippets=true&text=python&page=1

# очищаем файл перед заходом в цикл
path = "hh_all.rsp"
f = open(path, 'w')
f.close()

page_id = 37
while True:
    url = "https://hh.ru/search/vacancy"
    params = {
        'L_is_autosearch': 'false',
        'clusters': 'true',
        'enable_snippets': 'true',
        'text': vacancy,
        'page': page_id
    }
    headers = {
        'User-Agent': u.random
    }
    proxies = {
        'http': 'http://3.88.169.225:80',
        # 'https': 'https://165.227.223.19:3128',
    }
    # params['page'] = page_id
    answ = get(url, headers, params, proxies)
    save_pickle(answ, path)

    print("Страница ", page_id, "Последняя страница? ", next_page(answ))

  #  break

    if next_page(answ):
        break
    else:
        page_id = page_id + 1
        continue


path = "hh_all.rsp"
req = load_pickle(path)
soup = bs(req.text, 'html.parser')
# print(soup)

# вакансия
vacancy_info = soup.find_all(attrs={"data-qa": ["vacancy-serp__vacancy", "vacancy-serp__vacancy_premium"],
                                    "class": ["vacancy-serp-item", "vacancy-serp-item_premium"]

                                }#,
                             #limit=20
                             )
print(len(vacancy_info))

vacancies = []

for i_tag in vacancy_info:
    info = {}
    try:
        # название вакансии
        vacancy_name = i_tag.find(attrs={"class": "bloko-section-header-3 bloko-section-header-3_lite"}).text.replace('\xa0', '')
        # Ссылка на саму вакансию
        link = i_tag.find(attrs={"class": "g-user-content"}).a['href']
        # Сайт, откуда собрана вакансия
        resource = 'https://hh.ru/'
        # Предлагаемая зп
        zp = i_tag.find(attrs={"data-qa": "vacancy-serp__vacancy-compensation"}).text
        zp_min = zp_pars(zp)[0]
        zp_max = zp_pars(zp)[1]
        zp_curr = zp_pars(zp)[2]

        info['vacancy_name'] = vacancy_name
        info['link'] = link
        info['resource'] = resource
        # info['zp'] = zp
        info['zp_min'] = zp_min
        info['zp_max'] = zp_max
        info['zp_curr'] = zp_curr
        vacancies.append(info)
    except AttributeError:
        pass


pprint(vacancies)
print(len(vacancies))

with open("vacancies.json", "w") as f:
    json.dump(vacancies, f, indent=2, ensure_ascii=True)
