import praw
import datetime as dt
import fire
import json

# from apscheduler.schedulers.blocking import BlockingScheduler

from store import update_database
from store import logger


GENERATOR_LIMIT = 100
DEFAULT_OAUTH_LOC = '../../reddit-engagement-files/oauth.json'
DEFAULT_DB_LOC = '../../reddit-engagement-files/activity.db'

def launch_retrieval(redditor, mode, db_path=DEFAULT_DB_LOC, limit=GENERATOR_LIMIT):
    # only downvote/upvote retrieval supported now
    if mode == 'down':
        generator = redditor.downvoted(limit=limit)
    elif mode == 'up':
        generator = redditor.upvoted(limit=limit)
    else:
        raise ValueError('Cannot interpret mode', mode)

    # send generator to sqlite3 storage and log progress
    update_database(generator, mode, db_path)
    logger('Finished retrieval for %s mode' % mode)

def main(oauth_filepath=DEFAULT_OAUTH_LOC, db_path=DEFAULT_DB_LOC, first_launch=False):
    # connect to reddit
    connection_params = json.load(open(oauth_filepath, 'r'))
    reddit = praw.Reddit(**connection_params)
    redditor = reddit.user.me()

    # first-time info-dump
    if first_launch:
        launch_retrieval(redditor, 'down', limit=None)
        launch_retrieval(redditor, 'up', limit=None)

    # runtime connection issue fix unknown, currently avoiding error-handling until resolved
    # scheduler = BlockingScheduler()
    # scheduler.add_job(launch_retrieval, 'cron', args=[redditor, 'down', db_path], minute=0)
    # scheduler.add_job(launch_retrieval, 'cron', args=[redditor, 'up', db_path], minute=0)
    # scheduler.start()
    
    # schedule data retrieval for every start of hour manually, so can handle errors
    while True:
        if dt.datetime.now().minute == 0:
            try:
                launch_retrieval(redditor, 'down', db_path)
                launch_retrieval(redditor, 'up', db_path)
            except e:
                launch_retrieval(redditor, 'down', db_path)
                launch_retrieval(redditor, 'up', db_path)
            print(dt.datetime.now().hour)
            

if __name__ == '__main__':
    fire.Fire(main)
