# PUT YOUR LOGIN AND PASSWORD
# CHOOSE WHOSE FOLLOWERS YOU WANT TO FOLLOW
# AND PUT THEM IN A FOLLOW LIST IN APOSTROPHES AND SEPARATE WITH COMMAS
# HOW MANY PEOPLE TO FOLLOW PER DAY - BETTER NOT EXCEED 200 OR CAN BE BANNED

from functional import IgFollower

follower = IgFollower(login="your_login",
                 password="your_password",
                 follow_list=['blogger-whose-followers-to-follow',
                              'another-blogger',
                              'one-more-blogger'],
                 follow_per_day=100)
