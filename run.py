import sys
import praw
import time
from config import *


class C:
    green, red, white, yellow = '\033[92m', '\033[91m', '\033[0m', '\033[93m'


print(C.yellow + """
╔═╗╔═╗╔═╗╔╦╗╔╗ ╦ ╦╔═╗  ╦═╗╔═╗╔╦╗╔╦╗╦╔╦╗
║ ╦║ ║║ ║ ║║╠╩╗╚╦╝║╣   ╠╦╝║╣  ║║ ║║║ ║
╚═╝╚═╝╚═╝═╩╝╚═╝ ╩ ╚═╝  ╩╚═╚═╝═╩╝═╩╝╩ ╩
""")

try:
    r = praw.Reddit(client_id=client_id,
                    client_secret=client_secret,
                    user_agent=user_agent,
                    username=reddit_user,
                    password=reddit_pass)

    friends = r.user.friends()
    print(C.white + 'Sending {} messages to friends\n'.format(len(friends)))

    for friend in friends:
        try:
            if include_username:
                msg = message_text
            else:
                msg = message_text.format(friend)
            if test_mode:
                print(C.green + 'Messaging', str(friend), '[TEST MODE]')
            else:
                print(C.green + 'Messaging', str(friend))
                r.redditor(friend).message(message_title, msg)
        except Exception as e:
            print(C.red + e)

        time.sleep(timer)

    print(C.white + '\nDone\n')

except KeyboardInterrupt:
    print(C.white + '\nExiting\n')
    sys.exit()
except Exception as e:
    print(C.white + str(e))
