"""
This worker streams and parse tweets of certain candidates
"""
# coding: utf-8

# imports

import os
import datetime

import boto3

from TwitterAPI import TwitterAPI

import utils


# credentials
API_KEY = "41PE1Ven1SpvTH6IhgCXSfUrW"
API_SECRET = "dcDvnqexFNqg3FcB2D2ImUKFWQaSlYgoVNieHeM587bDiGIbo9"
ACCESS_TOKEN_KEY = "67362265-KwY3fHoxvlbfDUZ36lgZYxXS6pTS2bc7DjTgq9SPb"
ACCESS_TOKEN_SECRET = "kvW3Mqb4IQqYsLb4piwMbFyktaXXmvHwhYW8lJPGczCqC"


# api twitter
api = TwitterAPI(consumer_key=API_KEY,
                 consumer_secret=API_SECRET,
                 access_token_key=ACCESS_TOKEN_KEY,
                 access_token_secret=ACCESS_TOKEN_SECRET)


# Create an S3 client
client = boto3.client(
    's3',
    aws_access_key_id='AKIAITSLOEFRVYGULPKQ',
    aws_secret_access_key='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')


# today day in mexico object
today = utils.get_today_mex()


# function to download tweets
def download():

# tracking
    r = api.request('statuses/filter', {'track': ['@lopezobrador_',
                                                '@JoseAMeadeK',
                                                '@RicardoAnayaC',
                                                '@JaimeRdzNL',
                                                '@Mzavalagc',
                                                '@RiosPiterJaguar']})

    id = 0
    file = 'tweets.txt'

    with open(file, 'wb') as f:

        # setting a header
        header = u"/".join(['id', 'tweet_id', 'date', 'user_post', 'mention', 'location', 'tweet'])
        f.write(header.encode('UTF-8'))
        f.write(b'\n')

        for item in r:
            if 'text' in item:

                new_id = id  # setting id to control

                tweet_id = item['id_str']  # getting tweet id

                date = datetime.datetime.strptime(item['created_at'], '%a %b %d %H:%M:%S %z %Y')  #getting date
                date = utils.convert_to_mex(date)  # converting to mex date

                user = item['user']['screen_name']  # getting user

                location = item['coordinates']  # getting location

                mentions = {'mentions': []}
                for mention in item['entities']['user_mentions']:
                    mentions['mentions'].append(mention['screen_name'])  # getting all mentions inside the tweet

                tweet = item['text'].replace('\n','').replace('\t','')  #getting the tweet

                # final line
                new_line = [new_id, tweet_id, date, user, mentions, location, tweet]
                line = u'/'.join([str(i) for i in new_line])
                f.write(line.encode('UTF-8'))
                f.write(b'\n')

                id += 1

                if id % 10 == 0:
                    client.upload_file('tweets.txt', 'elecciones2018', 'tweets.txt')

            elif 'disconnect' in item:
                print('[disconnect] %s' % item['disconnect'].get('reason'))
                download()


# starting download
download()




