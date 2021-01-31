import praw
import datetime as dt
import fire
import json

from apscheduler.schedulers.blocking import BlockingScheduler

GENERATOR_LIMIT = 200

def launch_retrieval(redditor, mode):
    if mode == 'down':
        generator = redditor.downvoted(limit=GENERATOR_LIMIT)
    elif mode == 'up':
        generator = redditor.upvoted(limit=GENERATOR_LIMIT)
    else:
        raise ValueError('Cannot interpret mode', mode)
    timestamp = dt.datetime.now()
    print('%s %d %s' % (mode, len(list(generator)), timestamp))
    # call store function on generator
    # logger('info')

def launch_dashboard():
    raise NotImplementedError

def logger(info):
    raise NotImplementedError

def main(oauth_filepath):
    # connect to reddit
    connection_params = json.load(open(oauth_filepath, 'r'))
    reddit = praw.Reddit(**connection_params)
    redditor = reddit.user.me()

    # schedule data retrieval for every start of hour
    scheduler = BlockingScheduler()
    scheduler.add_job(launch_retrieval, 'cron', args=[redditor, 'down'], minute=0)
    scheduler.add_job(launch_retrieval, 'cron', args=[redditor, 'up'], minute=0)
    scheduler.start()
    
if __name__ == '__main__':
    fire.Fire(main)
