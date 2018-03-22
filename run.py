import time
import praw
import numpy as np
import matplotlib.pyplot as plt
import collections
import datetime
from dateutil.relativedelta import relativedelta
from halo import Halo
import argparse
from config import *


class C:
    green, red, white, yellow = '\033[92m', '\033[91m', '\033[0m', '\033[93m'

try:
    parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser(description="Reddit Flair Analytics (by /u/impshum)")
    parser.add_argument('-s', '--sub', help="Which subreddit to target", type=str)
    parser.add_argument('-m', '--months', help="How many months to get history of", type=int)
    parser.add_argument('-a', '--all', action='store_true', help="Pass this to get all history from the dawn of time")
    args = parser.parse_args()

    months_back = args.months
    all_history = args.all
    my_subreddit = args.sub

    if args.all:
        all_history = args.all
    else:
        all_history = False


    print(C.yellow + """
╔═╗╦  ╔═╗╦╦═╗  ╔═╗╔╗╔╔═╗╦ ╦ ╦╔╦╗╦╔═╗╔═╗
╠╣ ║  ╠═╣║╠╦╝  ╠═╣║║║╠═╣║ ╚╦╝ ║ ║║  ╚═╗
╚  ╩═╝╩ ╩╩╩╚═  ╩ ╩╝╚╝╩ ╩╩═╝╩  ╩ ╩╚═╝╚═╝
    """)
    print(C.white + 'Getting stats from /r/{}\n'.format(my_subreddit))

    reddit = praw.Reddit(client_id=client_id,
                         client_secret=client_secret,
                         user_agent=user_agent)

    count = {}
    score = {}
    comments = {}
    subreddit = reddit.subreddit(my_subreddit)

    counter = 0
    last = time.time()
    last_end = ''
    back_end = ''

    spinner = Halo(text='', spinner='dots')
    spinner.start()

    while True:

        if counter > 1:
            last_one = save_last()
            last = last_one - 10

        orig = datetime.datetime.fromtimestamp(last)
        new = orig - relativedelta(months=months_back)
        back = new.timestamp()

        if last == last_end and back == back_end:
            break

        back_end = back
        last_end = last
        last_r = datetime.datetime.utcfromtimestamp(last).strftime('%d-%m-%Y')
        back_r = datetime.datetime.utcfromtimestamp(back).strftime('%d-%m-%Y')

        msg = str(last_r) + ' - ' + str(back_r)
        spinner.text = msg

        def save_last():
            last = submission.created_utc
            return last

        for submission in subreddit.submissions(int(back), int(last)):
            # print(submission)
            #print(C.green + submission.title)

            if not submission.link_flair_text in count:
                count[submission.link_flair_text] = 0
            else:
                count[submission.link_flair_text] += 1

            if not submission.link_flair_text in score:
                score[submission.link_flair_text] = 0
            else:
                score[submission.link_flair_text] += submission.score

            if not submission.link_flair_text in comments:
                comments[submission.link_flair_text] = 0
            else:
                comments[submission.link_flair_text] += submission.num_comments

            counter += 1
            save_last()

        if not all_history:
            break

        time.sleep(6)

    def plot():
        spinner.text = 'Plotting graphs'
        plt.style.use('ggplot')
        plt.rcParams['font.size'] = 7
        x = np.arange(len(count))
        ax = plt.subplot(111)
        ax.bar(x - 0.2, count.values(), width=0.2, align='center')
        ax.bar(x, score.values(), width=0.2, align='center')
        ax.bar(x + 0.2, comments.values(), width=0.2, align='center')
        ax.legend(('Flair Count', 'Score', 'Comments'))
        plt.xticks(x, count.keys(), rotation=0)
        plt.tight_layout()
        plt.savefig("graphs/bar.png", dpi=300)
        # plt.show()

        itemz = collections.OrderedDict(count)
        count1 = []
        count2 = []

        for key, value in itemz.items():
            count1.append(key)
            count2.append(value)

        fig1, ax1 = plt.subplots()
        ax1.pie(count2, labels=count1, autopct='%1.1f%%',
                shadow=False, startangle=90)
        ax1.axis('equal')
        plt.tight_layout()
        plt.savefig("graphs/pi.png", dpi=300)
        # plt.show()


    plot()
    msg = 'Total posts: ' + str(counter - 1)
    spinner.succeed(msg)
    spinner.stop()

    print(C.green + '\nFlair count')
    for k, v in count.items():
        print(k, v)

    print(C.green + '\nScore count')
    for k, v in score.items():
        print(k, v)

    print(C.green + '\nComment count')
    for k, v in comments.items():
        print(k, v)

    print(C.white + '\nYour graphs have been saved to the graphs/ folder\n')

except Exception as e:
    print(C.red + str(e))
    print(C.white + '\nExiting\n')
except KeyboardInterrupt:
    print(C.white + '\nExiting\n')

