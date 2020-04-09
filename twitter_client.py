#!/usr/bin/env python3
"""
A standalone twitter client implementation
see https://tweepy.readthedocs.io/en/latest/
"""
import os
import sys
import datetime as dt
import time
import logging
import tweepy
from dotenv import load_dotenv

# Guard against python2
if sys.version_info[0] < 3:
    raise RuntimeError("Python 3 is required")

# Bring all keys and tokens from .env file into environment
load_dotenv()
exit_flag = False

# Create a local (module) logger instance
# YOUR CODE HERE


class TwitterClient(tweepy.StreamListener):
    """Customized TwitterClient class"""

    def __init__(self, consumer_key, consumer_secret,
                 access_token, access_token_secret):
        """Create a Tweepy API object using external tokens"""
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        # Creation of the twitter api client, using OAuth object.
        self.api = tweepy.API(auth)
        assert self.api is not None
        self.stream_handler = None

    def on_status(self, status):
        """Callback for receiving tweet messages"""
        # YOUR CODE HERE
        return True

    def register_stream_handler(self, func=None):
        """This allows an external function to hook into the twitter stream"""
        logger.info(f'Registering new stream handler: {func.__name__}')
        self.stream_handler = func

    def create_filtered_stream(self, track_list, retweets=False):
        # YOUR CODE HERE
        pass


def run_twitter_client(args):
    """This is for testing of standalone twitter client only"""

    logger.info("Starting TwitterClient")
    app_start = dt.now()

    # create a twitter client instance
    with TwitterClient(
        consumer_key=os.environ['CONSUMER_KEY'],
        consumer_secret=os.environ['CONSUMER_SECRET'],
        access_token=os.environ['ACCESS_TOKEN'],
        access_token_secret=os.environ['ACCESS_TOKEN_SECRET']
    ) as twit:

        # In real life, this would be the SlackClient registering it's own stream handler
        def my_handler(status):
            logger.info(status.text)
            return (not exit_flag)
        twit.register_stream_handler(my_handler)

        # begin receiving messages
        track_list = ['python']
        twit.create_filtered_stream(track_list)

        # wait for OS exit
        try:
            while not exit_flag:
                logger.debug('zzz ...')
                time.sleep(1.0)
        except KeyboardInterrupt:
            logger.warning('CTRL-C manual exit')

        uptime = dt.now() - app_start

    logger.warning(f'Shutdown completed, uptime: {uptime}')
    logging.shutdown()


if __name__ == '__main__':
    run_twitter_client(sys.argv[1:])
