import praw
import time 
import datetime as dt
import fire
import json

GENERATOR_LIMIT = 200

def launch_retrieval(redditor, mode):
    if mode == 'down':
        generator = redditor.downvoted(limit=GENERATOR_LIMIT)
    elif mode == 'up':
        generator = redditor.upvoted(limit=GENERATOR_LIMIT)
    else:
        raise ValueError('Cannot interpret mode', mode)
    # call store function on generator
    # logger(info)

def launch_dashboard():
    raise NotImplementedError

def logger(info):
    raise NotImplementedError

def main(oauth_filepath):
    connection_params = json.load(open(oauth_filepath, 'r'))
    reddit = praw.Reddit(**connection_params)
    redditor = reddit.user.me()

    # this should happen every 00, so sep fn to time this? or snippet here
    launch_retrieval(redditor, 'down')
    launch_retrieval(redditor, 'up')
    # this is first, time after this every 00
    
if __name__ == '__main__':
    fire.Fire(main)
