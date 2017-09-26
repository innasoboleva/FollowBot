from functional import IgFollower


user_agent3 = "Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14"

follower = IgFollower(login="bot_login",
                 password="bot_password", user_agnt=user_agent3)

follower.login()
follower.check_user_information()
follower.logout()