#!/bin/env python

#"Read the twitter feed from a text file and parse the text to filter out unicode and special characters"
from __future__ import division
import json
import re
import os
from datetime import datetime

UNICODED_TWT = []

def getTweet(full_tweet):
    #input should be of the json type
    try:
        raw_tweet = json.loads(full_tweet)
    except ValueError as e:
        return e

    if 'text' in raw_tweet:
        if re.search(r'[^\x00-\x7f]', raw_tweet['text']):
            UNICODED_TWT.append(raw_tweet['id'])
        clean_tweet = re.sub(r'[^\x00-\x7f]',r'', raw_tweet['text']).replace('\n', ' ').replace('\\', '')
        return clean_tweet + " (timestamp: " + str(raw_tweet['created_at']) + ")", raw_tweet['created_at']
    else:
        return '', ''

if __name__ == "__main__":

    #reading the twitter data stored in a file line break separated
    file_dir = os.path.dirname(os.path.realpath(__file__))
    os.chdir(file_dir)
    os.chdir('..')
    fbuf = open("data-gen/tweets.txt", 'r')
    outFile = open('tweet_output/ft1.txt', 'w')

    #running a loop on the text file that has json data obtained from the twitter API
    for fl in fbuf:

        #Question1: obtain the tweets data excluding any unicode's in the tweets.
        tweet, timestamp = getTweet(fl)
        if tweet:
            outFile.write(tweet + "\n")
    outFile.write("\n" + str(len(UNICODED_TWT)) + " tweets contained Unicode.")
    outFile.close()
    fbuf.close()
