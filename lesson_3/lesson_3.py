from pymongo import MongoClient


def vacancies_to_db(x):  # Функция для записи вакансий в базу данных
    client = MongoClient('127.0.0.1', 27017)
    db = client['ai_1054_vacancies']

    hh_vacancies = db.hh_vacancies

    hh_vacancies.insert_one(x)


def big_salary():  # Функция для печати вакансий с зп выше заданной
    client = MongoClient('127.0.0.1', 27017)
    db = client['ai_1054_vacancies']

    hh_vacancies = db.hh_vacancies
    my_salary = int(input('Enter your desired salary with digits: '))
    for i in hh_vacancies.find({}):
        if i['salary']['min'] > my_salary\
        or i['salary']['max'] > my_salary:
            print(i['name'], i['salary'])
