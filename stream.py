"""
This worker streams and parse tweets of certain candidates
"""
# coding: utf-8

# imports
import os
import datetime
import boto3
import utils
import schedule
import time

from TwitterAPI import TwitterAPI


# api twitter
api = TwitterAPI(consumer_key=os.environ['API_KEY'],
                 consumer_secret=os.environ['API_SECRET'],
                 access_token_key=os.environ['ACCESS_TOKEN_KEY'],
                 access_token_secret=os.environ['ACCESS_TOKEN_SECRET'])


# Create a S3 client
client = boto3.client(
    's3',
    aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'])



# function to download tweets
def download():

    # tracking
    r = api.request('statuses/filter', {'track': ['@lopezobrador_',
                                                  '@JoseAMeadeK',
                                                  '@RicardoAnayaC',
                                                  '@JaimeRdzNL',
                                                  '@Mzavalagc',
                                                  '@RiosPiterJaguar']})

    # today day in mexico object
    today = utils.get_today_mex()

    id_ = 0
    file = 'tweets-' + str(today.date()) + '.txt'

    with open(file, 'wb') as f:

        # setting a header
        header = u"/".join(['id', 'tweet_id', 'date', 'user_id',
                            'username', 'reply_to_user', 'reply_to_tweet',
                            'mention', 'location', 'lang', 'tweet'])
        f.write(header.encode('UTF-8'))
        f.write(b'\n')

        for item in r:
            if 'text' in item:

                # getting basic information for each tweet

                new_id = id_  # setting id to control

                tweet_id = item['id_str']  # getting tweet id

                date = datetime.datetime.strptime(
                    item['created_at'], '%a %b %d %H:%M:%S %z %Y')  # getting date of the tweet
                date = utils.convert_to_mex(date)  # converting to mex date

                user_id = item['user']['id']
                username = item['user']['screen_name']  # getting user

                reply_id = item['in_reply_to_user_id_str']  # in reply yo id
                reply_to = item['in_reply_to_status_id_str']

                location = item['coordinates']  # getting location

                lang = item['lang']     # getting language

                mentions = {'mentions': []}
                for mention in item['entities']['user_mentions']:
                    # getting all mentions inside the tweet
                    mentions['mentions'].append(mention['screen_name'])

                tweet = item['text'].replace('\n', '').replace(
                    '\t', '')  # getting the tweet

                # new line to append at the end
                new_line = [new_id, tweet_id, date, user_id,
                            username, reply_id, reply_to,
                            mentions, location, lang, tweet]
                line = u'/'.join([str(i) for i in new_line])
                f.write(line.encode('UTF-8'))
                f.write(b'\n')

                id_ += 1  # id + 1

                # sendinf file to S3 every 10 new tweet
                if id_ % 10 == 0:
                   client.upload_file(
                      file, 'elecciones2018', file)

            # if connection is broke, start again
            elif 'disconnect' in item:
                print('[disconnect] %s' % item['disconnect'].get('reason'))
                download()

# file per day
schedule.every().day.at("06:00").do(download)  # UTC time - 00:00 AM Mexico

while True:
    schedule.run_pending()
    time.sleep(1)




