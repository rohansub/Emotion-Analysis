from __future__ import print_function
import json
import unicodedata
from alchemyapi import AlchemyAPI
import numpy as np

#textFile_msg = ["Happy Bunnies!", "I hate life", "I love life"]
# textFile_post = [("I am okay","1235"),("I am not okay","1234"),("Hey guys!","1234")]
# textFile_tweet = [("Hey how are you?","1235"), ("I hate him", "1234"),("This is the best!","1234")]
alchemyapi = AlchemyAPI()

# code for fetching text to arrays

def PostData (textFile_post):
    stackPost = []
    tempList = []
    postCounter = 0
    postSum = 0.0
    curDate1 = textFile_post[0][1]
    for i in xrange(len(textFile_post)):
        response = alchemyapi.sentiment('html', textFile_post[len(textFile_post)-i-1][0])
        if response['status'] == 'OK':
            response['usage'] = ''
            if 'score' in response['docSentiment']:
    	           arb2 = float(unicode(response['docSentiment']['score']))
    	    #print(arb2)
            if textFile_post[i][1]==curDate1:
                postSum += arb2
                postCounter += 1
                tempList.append(arb2)
            else:
                #print("This branch is active")
                postAvg = (postSum/postCounter)*5.0 + 5.0
                postStdError = np.std(tempList)/float(np.sqrt(len(tempList)))
                tempList = []
                stackPost.append((postAvg,postStdError, textFile_post[len(textFile_post)-i][1],postCounter))
                postSum = arb2
                postCounter = 1
                curDate1 = textFile_post[len(textFile_post)-i-1][1]
            #print(arb2*5+5)
        else:
            print('Error in sentiment analysis call: ', response['statusInfo'])
    postAvg = (postSum/postCounter)*5.0 + 5.0
    postStdError = np.std(tempList)/float(np.sqrt(len(tempList)))
    tempList = []
    stackPost.append((postAvg,postStdError, textFile_post[len(textFile_post)-i-1][1],postCounter))

    # for i in xrange(len(stackPost)):
    #     #print('i = ',i,"out of ",len(stackPost))
    #     element = stackPost.pop()
    #     print(element)
    # Format {Rating, StdDev, Date, Counter}

    return stackPost


def TweetData (textFile_tweet):
    tweetCounter = 0
    tweetSum = 0.0
    tweetStdDev = 0.0
    tempList = []
    stackTweet = []
    curDate2 = textFile_tweet[0][1]
    for i in xrange(len(textFile_tweet)):
        response = alchemyapi.sentiment('html', textFile_tweet[len(textFile_tweet)-i-1][0])
        if response['status'] == 'OK':
            response['usage'] = ''
            if 'score' in response['docSentiment']:
    	           arb3 = float(unicode(response['docSentiment']['score']))
    	    #print(arb3)
            if textFile_tweet[len(textFile_tweet)-i-1][1]==curDate2:
                tweetSum += arb3
                tweetCounter += 1
                tempList.append(arb3)
            else:
                tweetAvg = (tweetSum/tweetCounter)*5 + 5
                tweetStdError = np.std(tempList)/float(np.sqrt(len(tempList)))
                tempList = []
                stackTweet.append((tweetAvg, tweetStdError, textFile_tweet[len(textFile_tweet)-i][1],tweetCounter))
                tweetSum = arb3
                tweetCounter = 1
                curDate2 = textFile_tweet[len(textFile_tweet)-i-1][1]
            #print(arb3*5+5)
        else:
            print('Error in sentiment analysis call: ', response['statusInfo'])
    tweetAvg = (tweetSum/tweetCounter)*5.0 + 5.0
    tweetStdError = np.std(tempList)/float(np.sqrt(n))
    tempList = []
    stackTweet.append((tweetAvg,tweetStdError, textFile_tweet[len(textFile_tweet)-i-1][1],tweetCounter))
    # for i in xrange(len(stackTweet)):
    #     #print('i = ',i,"out of ",len(stackTweet))
    #     element = stackTweet.pop()
    #     print(element)
    # Format {Rating, StdDev, Date, Counter}
    return stackTweet

def WeightedData (FbData, TwData):
    WData = []
    index = 0
    for i in xrange (0,len(FbData)):
        for j in xrange (0, len(TwData)):
            if (FbData[i][2] == TwData[j][2]):
                Nt = TwData[j][3]
                Nf = FbData[i][3]
                TwWeight =  (float(Nt))/(Nt+Nf);
                FbWeight =  (float(Nf))/(Nf+Nt);
                WData [i][0] = TwWeight * TwData[j][0] + FbWeight * FbData[i][0]
                WData [i][1] = (FbData[i][1] + TWData[j][1])/2.0
                WData [i][2] = FbData[i][2]
                break;
        if (FbData[i][2] < TwData[j][2]):
            WData.append(FbData[i])
        else:
            WData.append(TwData[i])
    return WData

def DecayData (WData):
    DecData = WData
    for i in xrange (4, len(WData)):
        maxDecError = max(WData[i][1], WData[i-1][1], WData[i-2][1], WData[i-3][1], WData[i-4][1])
        DecData[i][0] = WData[i][0] * 0.6 + WData[i-1][0] * 0.2 + WData[i-2][0] * 0.1 + WData[i-3][0] *0.05 + WData[i-4][0] *0.05
        DecData[i][1] = maxDecError;

    return DecData


    #Return Format {{Decayed Rating, Std Error, Date, Message Count}}

def CompositeAvg (DecData):
    AvgScore = 0
    sum = 0;
    for i in xrange (0, len(DecData)):
        sum += DecData[i][0]
    AvgScore = float(sum)/len(DecData)
    return AvgScore

def CompositeWk (DecData):
    AvgScore = 0
    sum = 0;
    for i in xrange (len(DecData)-5, len(DecData)):
        sum += DecData[i][0]
    AvgScore = float(sum)/5
    return AvgScore
