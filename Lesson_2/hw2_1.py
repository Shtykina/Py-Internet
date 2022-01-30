'''Необходимо собрать информацию о вакансиях на вводимую должность
(используем input или через аргументы получаем должность) с сайтов HH(обязательно)
и/или Superjob(по желанию). Приложение должно анализировать несколько страниц сайта
(также вводим через input или аргументы). Получившийся список должен содержать в себе минимум:
1.Наименование вакансии.
2.Предлагаемую зарплату (разносим в три поля: минимальная и максимальная и валюта. цифры преобразуем к цифрам).
3.Ссылку на саму вакансию.
4.Сайт, откуда собрана вакансия (можно указать статично для hh - hh.ru, для superjob - superjob.ru)
По желанию можно добавить ещё параметры вакансии (например, работодателя и расположение).
Структура должна быть одинаковая для вакансий с обоих сайтов. Общий результат можно вывести
с помощью dataFrame через pandas. Сохраните в json либо csv.'''

import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

url = 'https://hh.ru'
vacancy = 'Python junior'
page = 0
vacancies = []

while True:
    params = {'area': '113',
              'text': vacancy,
              'search_field': ['name', 'description'],
              'page': page}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/94.0.4606.85 YaBrowser/21.11.4.727 Yowser/2.5 Safari/537.36'}

    response = requests.get(url+'/search/vacancy', params=params, headers=headers)

    dom = BeautifulSoup(response.text, 'html.parser')

    vacancies_list = dom.find_all('div', {'data-qa': 'vacancy-serp__vacancy vacancy-serp__vacancy_standard_plus'})

    for position in vacancies_list:
        vacancy_data = {}

        info = position.find('a')
        name = info.getText()
        link = info.get('href')

        location = position.find('div', {'data-qa': 'vacancy-serp__vacancy-address'}).getText()
        company = position.find('a', {'data-qa': 'vacancy-serp__vacancy-employer'}).getText()

        site = url

        salary = position.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
        if not salary:
            salary_min = None
            salary_max = None
            currency = None
        else:
            data_salary = salary.getText().split(" ")
            if data_salary[0] == 'от':
                salary_min = re.sub(r'[^0-9]', '', data_salary[1])
                salary_min = int(salary_min)
                salary_max = None
                currency = data_salary[2]
            elif data_salary[0] == 'до':
                salary_min = None
                salary_max = re.sub(r'[^0-9]', '', data_salary[1])
                salary_max = int(salary_max)
                currency = data_salary[2]
            else:
                salary_min = re.sub(r'[^0-9]', '', data_salary[0])
                salary_max = re.sub(r'[^0-9]', '', data_salary[2])
                salary_min = int(salary_min)
                salary_max = int(salary_max)
                currency = data_salary[3]

        vacancy_data['name'] = name
        vacancy_data['salary_min'] = salary_min
        vacancy_data['salary_max'] = salary_max
        vacancy_data['currency'] = currency
        vacancy_data['location'] = location
        vacancy_data['company'] = company
        vacancy_data['link'] = link
        vacancy_data['site'] = site

        vacancies.append(vacancy_data)

    next_page = dom.find('a', {'data-qa': 'pager-next'})
    if next_page:
        page += 1
    else:
        break

df_vacancies = pd.DataFrame(vacancies)
print(df_vacancies.shape)
print(df_vacancies.loc[1])
df_vacancies.to_csv('hw2_1.csv', sep=";", encoding='utf-8')
