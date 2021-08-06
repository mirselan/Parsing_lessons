import requests
import json

# Получение с GitHub списка репозиториев пользователя mirselan:
url = 'https://api.github.com/users/mirselan/repos'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
                          AppleWebKit/537.36 (KHTML, like Gecko)\
                          Chrome/92.0.4515.107 Safari/537.36'}

response = requests.get(url, headers=headers)

j_data = response.json()

repos_list = []
for i in range(0, 6):
    repos_list.append(j_data[i]['name'])

print(f'The Mirselans repos on Github.com are: {repos_list}')

with open('j_data.json', 'w') as j_file:
    json.dump(j_data, j_file)
