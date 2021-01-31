import praw
import datetime as dt
import fire
import json

from apscheduler.schedulers.blocking import BlockingScheduler

from store import update_database
from store import logger


GENERATOR_LIMIT = 200
DEFAULT_OAUTH_LOC = '../../reddit-engagement-files/oauth.json'
DEFAULT_DB_LOC = '../../reddit-engagement-files/activity.db'

def launch_retrieval(redditor, mode, db_path=DEFAULT_DB_LOC):
    # only downvote/upvote retrieval supported now
    if mode == 'down':
        generator = redditor.downvoted(limit=GENERATOR_LIMIT)
    elif mode == 'up':
        generator = redditor.upvoted(limit=GENERATOR_LIMIT)
    else:
        raise ValueError('Cannot interpret mode', mode)

    # send generator to sqlite3 storage and log progress
    update_database(generator, mode, db_path)
    logger('Finished retrieval for %s mode' % mode)


def launch_dashboard():
    raise NotImplementedError

def main(oauth_filepath=DEFAULT_OAUTH_LOC, db_path=DEFAULT_DB_LOC):
    # connect to reddit
    connection_params = json.load(open(oauth_filepath, 'r'))
    reddit = praw.Reddit(**connection_params)
    redditor = reddit.user.me()

    # schedule data retrieval for every start of hour
    # scheduler = BlockingScheduler()
    # scheduler.add_job(launch_retrieval, 'cron', args=[redditor, 'down', db_path], minute=0)
    # scheduler.add_job(launch_retrieval, 'cron', args=[redditor, 'up', db_path], minute=0)
    # scheduler.start()

    # first time load way more, then do 200 at a time?
    launch_retrieval(redditor, 'down')

 
if __name__ == '__main__':
    fire.Fire(main)
