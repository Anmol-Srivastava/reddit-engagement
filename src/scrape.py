import praw
import datetime as dt
import fire
import json

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler

from store import update_database
from store import logger


GENERATOR_LIMIT = 100
DEFAULT_OAUTH_LOC = '../../reddit-engagement-files/oauth.json'
DEFAULT_DB_LOC = '../../reddit-engagement-files/activity.db'


def launch_retrieval(oauth_filepath, db_path, limit):
    # connect to reddit
    retries = 0
    while retries < 10:
        try:
            connection_params = json.load(open(oauth_filepath, 'r'))
            reddit = praw.Reddit(**connection_params)
            redditor = reddit.user.me()
            retries = 10
        except e:
            logger('Error at connection time.')
            print(repr(e))
            retries += 1
    
    # only downvote/upvote retrieval supported now
    retries = 0
    while retries < 10:
        try:
            upvote_gen = redditor.upvoted(limit=limit)
            downvote_gen = redditor.downvoted(limit=limit)
            retries = 10
        except e:
            logger('Error at generator time.')
            print(repr(e))
            retries += 1

    # send generator to sqlite3 storage and log progress
    retries = 0
    while retries < 10:
        try:
            update_database(upvote_gen, 'up', db_path)
            update_database(downvote_gen, 'down', db_path)
            retries = 10
        except e:
            logger('Internal error at storage time.')
            print(repr(e))
            retries += 1

    # attempt flushing
    retries = None
    connection_params = None
    redditor = None
    upvote_gen = None
    downvote_gen = None

    
def main(oauth_filepath=DEFAULT_OAUTH_LOC, db_path=DEFAULT_DB_LOC, first_launch=False):
    # first-time info-dump
    if first_launch:
        launch_retrieval(oauth_filepath, db_path, limit=None)

    # runtime connection issue fix unknown
    scheduler = BlockingScheduler()
    scheduler.add_job(launch_retrieval, 'cron', args=[oauth_filepath, db_path, GENERATOR_LIMIT], minute=0)
    scheduler.add_job(launch_retrieval, 'cron', args=[oauth_filepath, db_path, GENERATOR_LIMIT], minute=0)
    scheduler.start()


if __name__ == '__main__':
    fire.Fire(main)
