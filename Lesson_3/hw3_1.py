'''1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и
реализовать функцию, которая будет добавлять только новые вакансии в вашу базу.'''

import requests
from bs4 import BeautifulSoup
import re
from pymongo import MongoClient
from pymongo import errors
from pprint import pprint

client = MongoClient('127.0.0.1', 27017)

db = client['hh_vac_Python_junior']
vacancies = db.vacancies
vacancies.create_index('link', name='link_index', unique=True)

url = 'https://hh.ru'
vacancy = 'Python junior'
page = 0

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

        try:
            vacancies.insert_one(vacancy_data)
        except errors.DuplicateKeyError:
            pass

    next_page = dom.find('a', {'data-qa': 'pager-next'})
    if next_page:
        page += 1
    else:
        break

for vacancy_data in vacancies.find({}):
    pprint(vacancy_data)
