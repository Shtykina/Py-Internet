'''2.Написать функцию, которая производит поиск и выводит на экран вакансии
с заработной платой больше введённой суммы (необходимо анализировать оба поля зарплаты).
То есть цифра вводится одна, а запрос проверяет оба поля'''

from pymongo import MongoClient
from pprint import pprint

client = MongoClient('127.0.0.1', 27017)

db = client['hh_vac_Python_junior']
vacancies = db.vacancies

income = int(input('Income level from: '))

for vacancy_data in vacancies.find({'$or':
                             [{'salary_min': {'$gt': income}},
                              {'salary_max': {'$gt': income}}],
                              'currency': 'руб.'}):
    pprint(vacancy_data)

