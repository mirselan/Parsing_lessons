import requests
import json


url = 'https://api.vk.com'
access_token = '********it was my token***************************************************'
params = {'user_id': '**it was my id**',
          'extended': 1,
          'v': '5.124',
          'access_token': access_token}
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
                          AppleWebKit/537.36 (KHTML, like Gecko)\
                          Chrome/92.0.4515.107 Safari/537.36'}

response = requests.get(url + '/method/groups.get', params=params, headers=headers)

j_data = response.json()

groups_list = []
for i in range(0, 34):
    groups_list.append(j_data['response']['items'][i]['name'])

print(f'Мои группы ВК: {groups_list}')

with open('j_VK_data.json', 'w') as j_file:
    json.dump(j_data, j_file)
