from functional import IgFollower


user_agent2 = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 " \
                  "(KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36"


follower = IgFollower(login="bot_login",
                 password="bot_password", user_agnt=user_agent2)

follower.login()
follower.check_user_information()
follower.logout()