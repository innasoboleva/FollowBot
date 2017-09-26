# CHOOSE WHOSE FOLLOWERS YOU WANT TO FOLLOW
# AND PUT THEM IN A FOLLOW LIST IN APOSTROPHES AND SEPARATE WITH COMMAS LIKE THIS ['1 person', '2 person', '3 person']

from functional import IgFollower


user_agent1 = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6)' \
                 ' AppleWebKit/537.36 (KHTML, like Gecko)' \
                 ' Chrome/58.0.3029.110 Safari/537.36'

follower = IgFollower(login="bot_login", password="bot_password",
                      user_agnt=user_agent1, follow_list=['some_name'])

follower.login()
follower.make_a_list_to_check()
follower.check_user_information()
follower.logout()
