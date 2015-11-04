#!/bin/env python

#"Read the twitter feed from a text file and parse the text to filter out unicode and special characters"
from __future__ import division
import json
import re
import os
from datetime import datetime

UNICODED_TWT = []
HASHTAG_EDGE = []
HASHTAG_GRAPH = {}

def datediff(dt1, dt2):
    time1 = datetime.strptime(dt1, '%a %b %d %H:%M:%S +0000 %Y')
    time2 = datetime.strptime(dt2, '%a %b %d %H:%M:%S +0000 %Y')
    delta = time1 - time2
    return (delta.days * 86400)+delta.seconds

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

def getHashList(tweet):
    #running a loop to scan for all the hash-tags in the tweets
    hash_list = []
    for tweet_wd in tweet.split():
        #comparing if first character is #
        if re.match(r'^#', tweet_wd):
            if len(tweet_wd) > 1:
                hash_list.append(tweet_wd)
    return hash_list

def createTempEdgeList(hash_list):
    #creating a list of all possible edges from a tweet
    tempEdgeList = []
    hash_len = len(hash_list)
    for i in range(0, hash_len):
        for j in range(0, hash_len):
            if i != j:
                tempEdgeList.append([hash_list[i], hash_list[j]])
    return tempEdgeList

def delOlderEdges(timestamp):
    delEdges = []
    for entry in HASHTAG_EDGE:
        #identify all the edges older than 60 seconds
        if datediff(timestamp, entry[1]) > 60:
            delEdges.append(entry)

    for edges in delEdges:
        #deleting the edges older than 60 seconds from graph and edge list
        delEdgeFromGraph(edges[0])
        HASHTAG_EDGE.remove(edges)

def createListGraph(tmpEdgeList,timestamp):
    for edge in tmpEdgeList:
        #adding new edges from tweet to graph and edge List
        if HASHTAG_EDGE:
            hash_len = len(HASHTAG_EDGE)
            for entry in HASHTAG_EDGE:
                if entry[0][0] == edge[0] and entry[0][1] == edge[1]:
                    entry[1] = timestamp
                    break
                else:
                    hash_len -= 1
            if hash_len == 0:
                HASHTAG_EDGE.append([edge, timestamp])
                addEdgeToGraph(edge)
        else:
            HASHTAG_EDGE.append([edge, timestamp])
            addEdgeToGraph(edge)

def addEdgeToGraph(edge):
    #adding an edge to a graph
    #In this function it creates an edge or if the edge exists it appends a new edge
    if edge[0] in HASHTAG_GRAPH:
        HASHTAG_GRAPH[edge[0]].append(edge[1])
    else:
        HASHTAG_GRAPH[edge[0]] = [edge[1]]

def delEdgeFromGraph(edge):
    #Deleting an edge from a graph
    if edge[0] in HASHTAG_GRAPH:
        HASHTAG_GRAPH[edge[0]].remove(edge[1])
        if len(HASHTAG_GRAPH[edge[0]]) == 0:
            del HASHTAG_GRAPH[edge[0]]

def getAverageDegree(graph):
    #Getting average degree of the graph
    length = 0
    degree = 0
    for key in graph:
        length += 1
        degree += len(graph[key])
    if length == 0:
        return 0
    else:
        return format(degree / length, '.2f')


if __name__ == "__main__":

    #reading the twitter data stored in a file line break separated
    file_dir = os.path.dirname(os.path.realpath(__file__))
    os.chdir(file_dir)
    os.chdir('..')
    fbuf = open("data-gen/tweets.txt", 'r')
    #outFile = open('tweet_output/ft1.txt', 'w')
    outFile2 = open('tweet_output/ft2.txt', 'w')

    #running a loop on the text file that has json data obtained from the twitter API
    for fl in fbuf:

        #Question1: obtain the tweets data excluding any unicode's in the tweets.
        tweet, timestamp = getTweet(fl)
        #Maintain rolling 60 seconds window
        if timestamp:
            delOlderEdges(timestamp)
        if tweet:
            #outFile.write(tweet + "\n")
            hlist = getHashList(tweet)
            if len(hlist) > 1:
                tmpEdgeList = createTempEdgeList(hlist)
                createListGraph(tmpEdgeList, timestamp)
        average_degree = getAverageDegree(HASHTAG_GRAPH)
        outFile2.write(str(average_degree) + "\n")
    outFile2.close()
    fbuf.close()
