from psaw import PushshiftAPI
from datetime import datetime, timedelta, timezone
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
from requests import get
from halo import Halo
import pandas as pd
import argparse


def get_args():
    parser = argparse.ArgumentParser(
        description="Reddit Flair Analytics (by /u/impshum)",
        epilog='Example: run.py -s python -m 1')
    parser.add_argument(
        '-s', '--sub', help="Target subreddit", type=str)
    parser.add_argument(
        '-d', '--days', help="How many days", type=int)
    parser.add_argument(
        '-m', '--months', help="How many months", type=int)
    parser.add_argument(
        '-y', '--years', help="How many years", type=int)
    return parser.parse_args()


def search(sub, back):
    dt = datetime.now() - back
    timestamp = int(dt.replace(tzinfo=timezone.utc).timestamp())

    api = PushshiftAPI()
    gen = api.search_submissions(
        subreddit=sub, aggs='created_utc+link_flair_text+score+num_comments', after=timestamp)

    flairs = {}
    flair_scores = {}
    flair_count = {}
    flair_comment_count = {}

    c = 0

    for post in gen:
        created = datetime.fromtimestamp(post.created_utc).strftime('%d/%m/%Y')
        score = post.score
        num_comments = post.num_comments

        try:
            flair = post.link_flair_text
        except Exception:
            flair = 0
            pass

        if flair:
            flair_scores.update({flair: score})

            try:
                score = flair_scores[flair] + score
            except Exception:
                pass

            try:
                count = flair_count[flair] + 1
                flair_count.update({flair: count})
            except Exception:
                flair_count.update({flair: 1})

            try:
                if flair == 'RANT':
                    print(num_comments)

                new_comments = flair_comment_count[flair] + num_comments
                flair_comment_count.update({flair: new_comments})



            except Exception:
                flair_comment_count.update({flair: num_comments})

            spinner.text = f'{c}: Analysing posts from {created}'
            c += 1

    flairs.update({'score': flair_scores})
    flairs.update({'frequency': flair_count})
    flairs.update({'comments': flair_comment_count})

    df = pd.DataFrame(flairs)
    print(df)
    graphs(sub, df)


def graphs(sub, df):
    spinner.text = f'Building your graphs'

    df.plot.bar(figsize=(8, 8))
    plt.tight_layout(pad=5, w_pad=10, h_pad=10)
    plt.savefig(f'graphs/{sub}-bar.png')

    df.plot.pie(y='score', figsize=(8, 8))
    plt.tight_layout(pad=5, w_pad=10, h_pad=10)
    plt.savefig(f'graphs/{sub}-score-pie.png')

    df.plot.pie(y='frequency', figsize=(8, 8))
    plt.tight_layout(pad=5, w_pad=10, h_pad=10)
    plt.savefig(f'graphs/{sub}-frequency-pie.png')

    df.plot.pie(y='comments', figsize=(8, 8))
    plt.tight_layout(pad=5, w_pad=10, h_pad=10)
    plt.savefig(f'graphs/{sub}-comments-pie.png')

    spinner.succeed(f'All done. Have a nice day!')


def main():
    args = get_args()
    sub = args.sub
    years = args.years
    months = args.months
    days = args.days

    if years:
        back = relativedelta(years=years)
    elif months:
        back = relativedelta(months=months)
    elif days:
        back = relativedelta(days=days)
    else:
        spinner.fail(f'Enter correct arguments')

    if back:
        search(sub, back)

if __name__ == "__main__":
    spinner = Halo(text='Booting up', spinner='dots')
    spinner.start()
    main()
