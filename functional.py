# FUNCTIONAL FOR BOT-FOLLOWER
import requests
import json
import random
import time
import datetime


class IgFollower:

    url = 'https://www.instagram.com/'

    url_login = 'https://www.instagram.com/accounts/login/ajax/'
    url_logout = 'https://www.instagram.com/accounts/logout/'
    url_user = "https://www.instagram.com/{}/?__a=1"

    accept_encoding = 'gzip, deflate, sdch, br'
    accept_language = 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4'
    cache_control = 'public'
    origin = 'https://www.instagram.com'

    user_agent = ''

    error = 0
    error_ban = 3
    time_ban = 2 * 60 * 60

    login_status = False
    unfollow = True
    needs_check = True

    sleep_count = 0

    follow_counter = 0
    followed_users = []

    def __init__(self, login, password,
                 user_agnt='',
                 follow_list=[],
                 follow_per_day=200, bots=9
                 ):

        self.bots = bots
        self.follow_list = follow_list
        self.follow_per_day = follow_per_day
        self.time_in_day = 12 * 60 * 60
        self.sleep_delay = self.time_in_day / self.follow_per_day
        self.user_login = login.lower()
        self.user_password = password
        self.token = ''
        self.user_agent = user_agnt
        self.s = requests.Session()


    def find_user_id_and_num_follower(self, user):
        dictionary = []
        url_info = self.url_user.format(user)
        info = self.s.get(url_info)
        all_data = json.loads(info.text)
        id_user = all_data['user']['id']
        num_followers = all_data['user']['followed_by']['count']
        dictionary.append(id_user)
        dictionary.append(num_followers)
        print("Followers: " + str(num_followers))
        return dictionary

    def find_user_num_of_follower_and_following(self, user):
        dictionary = []
        url_info = self.url_user.format(user)
        try:
            info = self.s.get(url_info)
            all_data = json.loads(info.text)
            num_followers = all_data['user']['followed_by']['count']
            num_following = all_data['user']['follows']['count']
            dictionary.append(num_followers)
            dictionary.append(num_following)
        except:
            print('couldnt read data about user')
        return dictionary

    def getting_users_to_list(self, node_url, user, list_name):
        r = self.s.get(node_url.format(user))
        data = json.loads(r.text)
        nodes = data['data']['user']['edge_followed_by']['edges']
        for node in nodes:
            list_name[node['node']['username']] = node['node']['id']


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
        users_to_follow = {}
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

        print('Getting {} user\'s id'.format(user))
        users_id_and_fol = self.find_user_id_and_num_follower(user)
        print('User\'s id is ' + str(users_id_and_fol[0]))
        print("Number of followers: " + str(users_id_and_fol[1]))

        if users_id_and_fol[1] > 4000:
            for i in url_nodes:
                try:
                    self.getting_users_to_list(i, users_id_and_fol[0], users_to_follow)
                    print('Adding users...')
                except:
                    print('Adding users in a loop did not work.')
        else:
            try:
                self.getting_users_to_list(url_nodes[0], users_id_and_fol[0], users_to_follow)
                if len(users_to_follow) == 0:
                    self.getting_users_to_list(url_nodes[1], users_id_and_fol[0], users_to_follow)
                print('{} users are added without looping'.format(user))
            except:
                print('Adding users to a list did not work.')

        owners_id = self.find_user_id_and_num_follower(self.user_login)
        for i in url_followed:
            try:
                print('Now checking existing followers...')
                counter_followed_users = 0
                r = self.s.get(i.format(owners_id[0]))
                data = json.loads(r.text)
                nodes = data['data']['user']['edge_follow']['edges']
                for node in nodes:
                    followers_name = node['node']['username']
                    counter_followed_users += 1
                    if followers_name in users_to_follow:
                        print('Removing: ')
                        print(followers_name)
                        users_to_follow.pop(followers_name)
                print('From this round you have: ' + str(counter_followed_users) + ' users')
            except:
                print('Checking existing followers did not work.')

        return users_to_follow

    def make_a_list_to_check(self):
        future = open('data_follow_list', 'w+')
        future.close()
        one_more = open('data_followed', 'w+')
        one_more.close()
        and_more = open('chat', 'w+')
        and_more.close()
        for every_user in self.follow_list:
            my_list = self.user_list_for_fol(every_user)
            with open('check_file', 'w') as f:
                for key in my_list:
                    f.write(key)
                    f.write('\t')
                    f.write(my_list[key])
                    f.write('\n')

    def read_from_a_list(self):
        f = open('check_file', 'r+')
        temp_read_name = f.readline()
        if not temp_read_name:
            print('HORAAAAY. Check done!')
            self.needs_check = False
            f.close()
            text = "Done\n"
            self.write_to_data_list(text, 'chat')
            return
        f.seek(0)
        temp_lines = f.readlines()
        f.seek(0)
        for line in temp_lines:
            if line != temp_read_name:
                f.write(line)
        f.truncate()
        f.close()
        list_with_info = temp_read_name.split('\t')
        return list_with_info

    def check_user_information(self):
        while self.needs_check:
            name = self.read_from_a_list()
            try:
                info_about_user = self.find_user_num_of_follower_and_following(name[0])
                print('CHECKING -- ' + name[0])
                try:
                    if self.night_time_check_and_sleep():
                        print("Its night. GO TO BED!")
                        time.sleep((random.random() * 2 * 60 * 60) + 8 * 60 * 60)
                    else:
                        time.sleep(random.randint(60, 300))
                except:
                    print('time problems')
                if info_about_user[0] < 2000 and info_about_user[1] < 500:
                    self.write_to_data_list(name[1], 'data_follow_list')
            except:
                print('Could not check users data or the work is done!')

    def write_to_data_list(self, name, list_for_writing):
        with open(list_for_writing, 'a') as f:
            f.write(name)

    def night_time_check_and_sleep(self):
        now = datetime.datetime.now().time()
        if now >= datetime.time(22, 0, 0, 0) or now <= datetime.time(8, 0, 0, 0):
           return True
        else:
           return False

    def follow_and_unfollow(self):
        while True:
            f = open('data_follow_list', 'r+')
            temp_read_name = f.readline()

            if not temp_read_name and self.sleep_count < 3:
                print("Users are getting checked... Will wait a bit")
                self.sleep_count += 1
                time.sleep((random.random() * 5 * 60) + 5 * 60)
                continue
            elif not temp_read_name and self.sleep_count >= 3:
                self.sleep_count = 0
                chat = open('chat', 'r')
                keep_going = chat.readlines()
                if len(keep_going) == self.bots:
                    f.close()
                    chat.close()
                    print("HORAAAAY. Check done!")
                    break
                else:
                    chat.close()
                    continue
            f.seek(0)
            temp_lines = f.readlines()
            f.seek(0)
            for line in temp_lines:
                if line != temp_read_name:
                    f.write(line)
            f.truncate()
            f.close()
            temp_read = temp_read_name.rstrip()
            print('I READ FOR FOLLOW ' + temp_read_name)

            url_follow = 'https://www.instagram.com/web/friendships/{}/follow/'.format(temp_read)
            try:
                follow = self.s.post(url_follow)
                if follow.status_code == 200:
                    self.follow_counter += 1
                    self.followed_users.append(temp_read)
                    print('Followed {}'.format(temp_read_name))

                    self.write_to_data_list(temp_read_name, 'data_followed')
                    print('Going to sleep now.')
                    if self.night_time_check_and_sleep():
                        print("It is night. GO TO BED!")
                        time.sleep((random.random() * 2 * 60 * 60) + 8 * 60 * 60)
                    else:
                        time.sleep(self.sleep_delay * 0.9 + self.sleep_delay * 0.2 * random.random())

                    if self.unfollow:
                        while self.follow_counter >= self.follow_per_day * 2:

                            print("Users reached our daily limit, time to unfollow...")
                            url_unfollow = 'https://www.instagram.com/web/friendships/{}/unfollow/'.format(self.followed_users[-1])
                            try:
                                unfollow = self.s.post(url_unfollow)
                                if unfollow.status_code == 200:
                                    self.follow_counter -= 1
                                    print('Unfollowed {}'.format(self.followed_users[-1]))
                                    del self.followed_users[0]
                                    print('Going to sleep now.')
                                    if self.night_time_check_and_sleep():
                                        print("Its night. GO TO BED!")
                                        time.sleep((random.random() * 2 * 60 * 60) + 8 * 60 * 60)
                                    else:
                                        time.sleep(self.sleep_delay * 0.9 + self.sleep_delay * 0.2 * random.random())
                                elif unfollow.status_code == 400:
                                    print('Did not unfollow, code 400.')
                                    self.code_400()
                            except:
                                print("Except on unfollow!")

                elif follow.status_code == 400:
                    print("Did not follow, code 400.")
                    self.code_400()
                else:
                    print("Could not open the follow page. User is lost...")
            except:
                print("Except on follow!")

    def unfollow_users(self):
        print("Users reached our daily limit, time to unfollow...")
        url_unfollow = 'https://www.instagram.com/web/friendships/{}/unfollow/'.format(self.followed_users[-1])
        try:
            unfollow = self.s.post(url_unfollow)
            if unfollow.status_code == 200:
                self.follow_counter -= 1
                print('Unfollowed {}'.format(self.followed_users[-1]))
                del self.followed_users[0]
                print('Going to sleep now.')
                time.sleep(self.sleep_delay * 0.9 + self.sleep_delay * 0.2 * random.random())
            elif unfollow.status_code == 400:
                print('Did not unfollow, code 400.')
                self.code_400()
        except:
            print("Except on unfollow!")

    def logout(self):
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
