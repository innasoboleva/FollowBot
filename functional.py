# FUNCTIONAL FOR BOT-FOLLOWER

import requests
import json
import random
import time


class IgFollower:

    url = 'https://www.instagram.com/'

    url_login = 'https://www.instagram.com/accounts/login/ajax/'
    url_logout = 'https://www.instagram.com/accounts/logout/'
    url_user = "https://www.instagram.com/{}/?__a=1"

    accept_encoding = 'gzip, deflate, sdch, br'
    accept_language = 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4'
    cache_control = 'public'
    origin = 'https://www.instagram.com'
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6)' \
                 ' AppleWebKit/537.36 (KHTML, like Gecko)' \
                 ' Chrome/58.0.3029.110 Safari/537.36'

    error = 0
    error_ban = 3
    time_ban = 2 * 60 * 60

    login_status = False
    unfollow = True

    follow_counter = 0
    followed_users = []

    def __init__(self, login, password,
                 follow_list=[],
                 follow_per_day=0,
                 ):

        self.follow_list = follow_list
        self.follow_per_day = follow_per_day
        self.time_in_day = 24 * 60 * 60
        self.sleep_delay = self.time_in_day / self.follow_per_day
        self.user_login = login.lower()
        self.user_password = password
        self.token = ''
        self.s = requests.Session()
        # CALLING FUNCTIONS FOR IG_FOLLOWER TO WORK
        self.login()
        self.follow_users()
        self.logout()

    def find_user_id(self, user):
        url_info = self.url_user.format(user)
        info = self.s.get(url_info)
        all_data = json.loads(info.text)
        id_user = all_data['user']['id']
        return id_user

    def find_user_num_of_follower(self, user):
        url_info = self.url_user.format(user)
        info = self.s.get(url_info)
        all_data = json.loads(info.text)
        num_followers = all_data['user']['followed_by']['count']
        return num_followers

    def getting_nodes(self, node_url, user, list):
        r = self.s.get(node_url.format(user))
        data = json.loads(r.text)
        nodes = data['data']['user']['edge_followed_by']['edges']
        for node in nodes:
            list.add(node['node']['id'])

    def login(self):
            print('Let\'s log in as {}...\n'.format(self.user_login))
            self.s.headers.update({'accept-encoding': self.accept_encoding,
                                   'accept-language': self.accept_language,
                                   'cache_control': self.cache_control,
                                   'host': 'www.instagram.com',
                                   'origin': self.origin,
                                   'referer': self.origin,
                                   'user-agent': self.user_agent,
                                   'x-instagram-ajax': '1',
                                   'x-requested-with': 'XMLHttpRequest'})
            r = self.s.get(self.url)
            self.s.headers.update({'x-csrftoken': r.cookies['csrftoken']})
            time.sleep(7 * random.random())
            login = self.s.post(self.url_login, data=
            {'username': self.user_login, 'password': self.user_password},
                                allow_redirects=True)
            self.token = login.cookies['csrftoken']
            self.s.headers.update({'x-csrftoken': self.token})
            time.sleep(7 * random.random())

            if login.status_code == 200:
                r = self.s.get('https://www.instagram.com/')
                finder = r.text.find(self.user_login)
                if finder != -1:
                    self.login_status = True
                    print('{} logged in successfully!'.format(self.user_login))
                else:
                    self.login_status = False
                    print('Login error.')
            else:
                print('Login error. Try again.')
            print('\nGoing to follow some people now......\n')

    def user_list_for_fol(self, user):
        users_to_follow = set()
        url_nodes = ['https://www.instagram.com/graphql/query/?query_id=17851374694183129&id={}&first=4000',
                     'https://www.instagram.com/graphql/query/?query_id=17851374694183129&id={}'
                     '&first=3000&after=AQAuODyN1Ijd4jF2cCk1lEvvzZVMj0zY5z7HAvYjgimcULkEsLD5-9Z'
                     '_fL5ziAksC15bhF2mHug4NaZOu31sNi805iEau3KmzbSdcTeeZUVb-A',
                     'https://www.instagram.com/graphql/query/?query_id=17851374694183129&id={}'
                     '&first=3000&after=AQAlT3VL2doRrdWUYF-u5jiNBbSxdEJegIQY_Wn1SyDZoahq-IoYJL-'
                     '0P8agynYpxkqqHAjirLOBJUO9HF6unFEnF6PApO0bLGyyo1UroD05iA',
                     'https://www.instagram.com/graphql/query/?query_id=17851374694183129&id={}'
                     '&first=3000&after=AQDAdUhh0eouxqgORVmAMYF-wSSPHwmAjotXmyleYK5UfdXCLWTJuX'
                     'b1NFEoJsKalDLSOIBjuSDXESWTr0qVGVfYEDO9H1eLvtWPDSA-01gezA',
                     'https://www.instagram.com/graphql/query/?query_id=17851374694183129&id={}'
                     '&first=3000&after=AQDUKAahtakE3ajjavacHLItlXUON0QD1kyQwA1lC3se384L0VmwrZa'
                     '0YzA4_Z9oaNXklJjHXLDoPuXW08Y8eG8h2N83_N1EoEk8lxmvQKV3YQ']

        url_followed = ['https://www.instagram.com/graphql/query/?query_id=17874545323001329&id={}&first=1000',
                        'https://www.instagram.com/graphql/query/?query_id=17874545323001329&id={}'
                        '&first=1000&after=AQCFOtHdRh4ca3puR3nY07ZuDGqjNcKPeXJHUgvJ3ka0pJk-c0BOzo5'
                        'RhB2a3XxqWCdprCniR3jUqp_OVAfbThflbavhcjDrGoFp3S7j1a_5Uw',
                        'https://www.instagram.com/graphql/query/?query_id=17874545323001329&id={}'
                        '&first=1000&after=AQAmc8mg5Shs3v0Gq1xukoKuuNsem4d_LOYo-kYb0MWotlbZkynpYS'
                        'cvbaoD6BlX-9qtdUQy-LekiRUy4q6AhBRDvmJ5WjrrKSFJUnioLU4nkg',
                        'https://www.instagram.com/graphql/query/?query_id=17874545323001329&id={}'
                        '&first=1000&after=AQCbMJO2X_dwAMFobpcDS0w3Q9sn_1U04TSDQjHw2hhJYTEl9Dh6DpwC'
                        'Rg0VpSxv3sInt4Gl5eGQEDj_yMPejNfGGoYIXV7DgdYrIyBgCf-ryg']
        try:
            print('Getting {} user\'s id'.format(user))
            users_id = self.find_user_id(user)
            print('User\'s id is ' + str(users_id))
        except:
            print('Getting id did not work')
        try:
            print('Getting number of followers...')
            num_of_followers = self.find_user_num_of_follower(user)
            print("Number of followers: " + str(num_of_followers))
            if num_of_followers > 4000:
                for i in url_nodes:
                    self.getting_nodes(i, users_id, users_to_follow)
                    print('Adding users...')
            else:
                self.getting_nodes(url_nodes[0], users_id, users_to_follow)
                if len(users_to_follow) == 0:
                    self.getting_nodes(url_nodes[1], users_id, users_to_follow)
                print('{} users are added without looping'.format(user))
        except:
            print('Adding users to a list did not work.')
        try:
            print('Now checking existing followers...')
            for i in url_followed:
                counter_followed_users = 0
                owners_id = self.find_user_id(self.user_login)
                r = self.s.get(i.format(owners_id))
                data = json.loads(r.text)
                nodes = data['data']['user']['edge_follow']['edges']
                for node in nodes:
                    followers_id = node['node']['id']
                    counter_followed_users += 1
                    if followers_id in users_to_follow:
                        users_to_follow.remove(followers_id)
                        print('Removing: ')
                        print(followers_id)
                print('From this round you have: ' + str(counter_followed_users) + ' users')
        except:
            print('Checking existing followers did not work.')
        print('We need to follow: ')
        print(len(users_to_follow))
        return users_to_follow

    def follow_users(self):
        if self.login_status:
            new_list_to_follow = []
            for every_user in self.follow_list:
                users_to_follow = self.user_list_for_fol(every_user)
                for i in users_to_follow:
                    new_list_to_follow.append(i)
            for each_user in new_list_to_follow:
                url_follow = 'https://www.instagram.com/web/friendships/{}/follow/'.format(each_user)
                try:
                    follow = self.s.post(url_follow)
                    if follow.status_code == 200:
                        self.follow_counter += 1
                        self.followed_users.append(each_user)
                        print('Followed {}'.format(each_user))
                        print('Going to sleep now.')
                        time.sleep(self.sleep_delay * 0.9 + self.sleep_delay * 0.2 * random.random())
                        if self.unfollow:
                            self.unfollow_users()
                    elif follow.status_code == 400:
                        print('Did not follow, code 400.')
                        self.code_400()
                except:
                    print("Except on follow!")
            print('Followed everyone!')

    def unfollow_users(self):
        if self.login_status:
            while self.follow_counter >= self.follow_per_day * 2:
                print("Users reached our daily limit, time to unfollow...")
                for user in self.followed_users[::-1]:
                    url_unfollow = 'https://www.instagram.com/web/friendships/{}/unfollow/'.format(user)
                try:
                    unfollow = self.s.post(url_unfollow)
                    if unfollow.status_code == 200:
                        self.follow_counter -= 1
                        self.followed_users.remove(user)
                        print('Unfollowed {}'.format(user))
                        print('Going to sleep now.')
                        time.sleep(self.sleep_delay * 0.9 + self.sleep_delay * 0.2 * random.random())
                    elif unfollow.status_code == 400:
                        print('Did not unfollow, code 400.')
                        self.code_400()
                except:
                    print("Except on unfollow!")

    def logout(self):
        print('Followed: ' + str(self.follow_counter))
        try:
            self.s.post(self.url_logout)
            self.s.cookies.clear()
            print("Logout success!")
            self.login_status = False
        except:
            print("Logout error!")

    def code_400(self):
        if self.error >= self.error_ban:
            time.sleep(self.time_ban)
        else:
            self.error += 1
