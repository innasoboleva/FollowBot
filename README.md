# FollowBot
Repository for bot-follower for instagram

Bot includes:
 instagram_bot file -- runs your profile page and follows
 check_bot (from 1 to 9) files -- runs check on people, who you want to follow (you can create more check_bots if you'd like)
 functional file -- code for this class

 1. Put your login and password in instagram_bot.py.
 2. Create 9 different accounts for checking people whom you wish to follow,
    and put logins and passwords in defferent "check_bot.py" files.
 3. Put list of people you want to follow to check_bot1 file. And make sure
    this file runs first.

Everything runs synchronized. Check-bots check information about followers
(default follow works on people who are following less then 500 and whose followers are less then 2000).
Check bots store users to follow in a list. And main bot takes users from that list and follows until every
checked user from follow_list is followed.

If accidentally program quits or interrupted, you can check followed users in a file "data_followed" and users yet to be checked in "check_file" and users after the check yet to be followed in "data_follow_list".

# How to use this program
You will need 10 different terminal windows.
After putting logins and passwords and list of people to follow, run check_bot1.py file first, like this: "python3 check_bot1.py".
Wait until it gets all the information and starts checking. You will see “CHECKING -- some_name” in the console.
Now you can run all other bots in other terminal windows to help collect the information. Run instagram_bot as well to start following people.

Collecting information takes some time, don’t expect to see immediate results. 
Bots work on a safe side.

# Libraries
Install request module, for example on Mac in terminal run: "pip3 install requests".
