# Reddit Flair Analytics

Python bot to analyse a subreddit history and create pretty graphs from the results.

![Screenshot](https://i.imgur.com/pirXgWL.png)

### Install dependencies

    pip3 install -r requirements.txt

### Fill in the blanks     

Enter all your juicy details into config.py

### Arguments

* -h, --help            Show this help message and exit
* -s , --sub            Which subreddit to target
* -m , --months     How many months to get history of
*  -a, --all                Pass this to get all history from the dawn of time

### Run it

Get 6 month of data from /r/fpvracing

    python3 run.py -m 6 -s fpvracing

Get all data from /r/fpvracing in 1 month chunks

    python3 run.py -a -m 1 -s fpvracing
