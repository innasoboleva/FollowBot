"""
Bot includes:
 instagram_bot file -- runs your profile page and follows
 check_bot (from 1 to 9) -- runs check on people, who you want to follow (you can create more check_bots if you'd like)
 functional -- code for this class

 1. Put you login and password in instagram_bot
 2. Create 9 different account for checking people whom you wish to follow,
    and put logins and passwords in files called check_bot
 3. Put list of people you want to follow to check_bot1 file. And make sure
    this file opens first.

This way everything runs synchronized. Check-bots check information about followers
(default follow works on people who are following less then 500 and whose followers less then 2000).
Check bots store users to follow in a list. And main bot takes users from that list and follows until every
checked user from follow_list is followed.

If accidentally program quits or interrupted,
you can check followed users in a file "data_followed" and users yet to be checked in "check_file"
and users after the check yet to be followed in "data_follow_list".
"""

# PUT YOUR LOGIN AND PASSWORD

# HOW MANY PEOPLE TO FOLLOW PER DAY - BETTER NOT EXCEED 200 OR CAN BE BANNED

# PUT THE NUMBER OF BOTS WHICH YOU USE (9 BY DEFAULT, YOU CANNOT PUT 0 - PROGRAM WILL NOT WORK)

from functional import IgFollower

user_agent1 = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6)' \
                 ' AppleWebKit/537.36 (KHTML, like Gecko)' \
                 ' Chrome/58.0.3029.110 Safari/537.36'

follower = IgFollower(login="your_login",
                 password="your_password",
                 user_agnt=user_agent1, follow_per_day=200, bots=9)

follower.login()
follower.follow_and_unfollow()
follower.logout()
