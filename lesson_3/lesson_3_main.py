from bs4 import BeautifulSoup as bs
import requests
import lesson_3


def hh_vacancies():
    my_vacancy = input('Input your desired vacancy: ')
    page_num = 0
    while page_num != '':
        url = 'https://hh.ru'
        params = {
            'clusters': 'true',
            'no_magic': 'true',
            'ored_clusters': 'true',
            'enable_snippets': 'true',
            'st': 'searchVacancy',
            'text': f'{my_vacancy}',
            'from': 'suggest_post',
            'page': f'{page_num}'
        }
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
                                  AppleWebKit/537.36 (KHTML, like Gecko)\
                                  Chrome/90.0.4430.93 Safari/537.36'}

        response = requests.get(url+'/search/vacancy', params=params, headers=headers)
        if response.ok:
            soup = bs(response.text, 'html.parser')
            vacancies_list = soup.find_all('div', {'class': 'vacancy-serp-item'})

            def salary_dev(x):
                salary_data = {}  # Словарь для хранения полученных данных
                if x != '':
                    val = x.split()[-1]  # Извлечение валюты
                    num_min = 0
                    num_max = 0

                    if '–' in x:  # Извлечение мин и макс зарплаты, если есть оба значения
                        num = x.split('–')
                        num_min = int((''.join(i for i in num[0] if i.isdigit())))
                        num_max = int((''.join(i for i in num[1] if i.isdigit())))
                    elif 'от' in x:  # Извлечение мин зарплаты, если есть одно значение
                        num_min = int((''.join(i for i in x if i.isdigit())))
                    elif 'до' in x:  # Извлечение макс зарплаты, если есть одно значение
                        num_max = int((''.join(i for i in x if i.isdigit())))
            # Заполнение словаря
                    salary_data['min'] = num_min
                    salary_data['max'] = num_max
                    salary_data['carency'] = val
                else:
                    salary_data['min'] = 0
                    salary_data['max'] = 0
                    salary_data['carency'] = None
                return salary_data

            for vacancy in vacancies_list:
                vacancy_data = {}
                vacancy_info = vacancy.find('a', {'class': 'bloko-link'})
                vacancy_name = vacancy_info.getText()
                vacancy_url = vacancy_info.get('href')
                vacancy_salary = vacancy.find('div', {'class': 'vacancy-serp-item__sidebar'}).getText()
                vacancy_salary_dev = salary_dev(vacancy_salary)
                site_url = url

                vacancy_data['name'] = vacancy_name
                vacancy_data['url'] = vacancy_url
                vacancy_data['salary'] = vacancy_salary_dev
                vacancy_data['site_url'] = site_url

                lesson_3.vacancies_to_db(vacancy_data)

            page_num += 1
        else:
            break


hh_vacancies()
lesson_3.big_salary()
