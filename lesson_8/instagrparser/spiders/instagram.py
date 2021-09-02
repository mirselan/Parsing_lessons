import scrapy
import re
import json
from scrapy.http import HtmlResponse
from urllib.parse import urlencode
from copy import deepcopy
from instagrparser.items import InstagrparserItem


class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['https://www.instagram.com']
    insta_login = 'Onliskill_udm'
    insta_pass = '#PWD_INSTAGRAM_BROWSER:10:1629825416:ASpQAMvl1EAdo0NdRZNcM1/pjlU9rRg4n4cjCM00SDGSV5pDN6XbC93ZbYN67HUOHkXZnGGe2gIWPU2qtQY0HAkIjR5U5syu+lv8qtqeI7cyy2ua6WmBV6AngVo1apn3eJ6O3UAFVgb+q5HtHsQ='
    insta_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    user_parse = ['vrealiteclub19', 'maksim.alekseevich.pro']
    api_url = 'https://i.instagram.com/api/v1/friendships/'
    friends_type = ['followers', 'following']

    def parse(self, response: HtmlResponse):
        csrf = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(self.insta_login_link,
                                 method='POST',
                                 callback=self.user_login,
                                 formdata={'username': self.insta_login,
                                           'enc_password': self.insta_pass},
                                 headers={'X-CSRFToken': csrf})

    def user_login(self, response: HtmlResponse):
        j_body = response.json()
        if j_body['authenticated']:
            for i in self.user_parse:
                yield response.follow(f'/{i}',
                                      callback=self.user_data_parse,
                                      cb_kwargs={'username': i})

    def user_data_parse(self, response: HtmlResponse, username):
        user_id = self.fetch_user_id(response.text, username)
        variables = {'count': 12}
        headers = {'User-Agent': 'Instagram 155.0.0.37.107'}
        for i in self.friends_type:
            url_friends = f'{self.api_url}{user_id}/{i}/?{urlencode(variables)}'

        yield response.follow(url_friends,
                              callback=self.user_friends_parse,
                              headers=headers,
                              cb_kwargs={'username': username,
                                         'user_id': user_id,
                                         'variables': deepcopy(variables)}
                              )

    def user_friends_parse(self, response: HtmlResponse, username, user_id, variables):
        if response.status == 200:
            j_data = response.json()
            if j_data.get('next_max_id'):
                variables['max_id'] = j_data.get('next_max_id')
                variables['search_surface'] = 'follow_list_page'
                headers = {'User-Agent': 'Instagram 155.0.0.37.107'}
                url_friends = f'{self.api_url}{user_id}/{self.friends_type[0]}/?{urlencode(variables)}'

                yield response.follow(url_friends,
                                      callback=self.user_friends_parse,
                                      headers=headers,
                                      cb_kwargs={'username': username,
                                                 'user_id': user_id,
                                                 'variables': deepcopy(variables)})

            friends = j_data.get('users')
            for friend in friends:
                item = InstagrparserItem(user_id=friend.get('pk'),
                                         username=friend.get('username'),
                                         full_name=friend.get('full_name'),
                                         picture=friend.get('profile_pic_url'),
                                         friend_data=friend
                                         )
                yield item

    # Получаем токен для авторизации
    def fetch_csrf_token(self, text):
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    # Получаем id желаемого пользователя
    def fetch_user_id(self, text, username):
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')

