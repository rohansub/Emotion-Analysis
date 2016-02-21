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
    arb2 = 0
    curDate1 = textFile_post[len(textFile_post)-1][1]
    print('Facebook Time')
    for i in reversed(xrange(len(textFile_post))):
        response = alchemyapi.sentiment('html', textFile_post[i][0].encode('ascii','ignore'))
        if response['status'] == 'OK':
            response['usage'] = ''
            if 'score' in response['docSentiment']:
    	           arb2 = float(unicode(response['docSentiment']['score']))
    	    #print(textFile_post[i][1])
            #print(curDate1)
            if textFile_post[i][1]==curDate1:
                postSum += arb2
                postCounter += 1
                #print(postCounter)
                tempList.append(arb2)
            else:
                #print("This branch is active")
                if postCounter == 0:
                    postCounter == 1;
                postAvg = (postSum/postCounter)*5.0 + 5.0
                print(postAvg)
                postStdError = np.std(tempList)/float(np.sqrt(len(tempList)))
                tempList = []
                if i == len(textFile_post)-1:
                    stackPost.append((postAvg,postStdError, textFile_post[i][1],postCounter))
                else:
                    stackPost.append((postAvg,postStdError, textFile_post[i+1][1],postCounter))
                postSum = arb2
                postCounter = 1
                curDate1 = textFile_post[i][1]
            #print(arb2*5+5)
        else:
            print('Error in sentiment analysis call: ', response['statusInfo'])
    postAvg = (postSum/postCounter)*5.0 + 5.0
    print(postAvg)
    postStdError = np.std(tempList)/float(np.sqrt(len(tempList)))
    tempList = []
    stackPost.append((postAvg,postStdError, textFile_post[i][1],postCounter))

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
    curDate2 = textFile_tweet[len(textFile_tweet)-1][1]
    arb3 = 0
    print('Twitter Time')
    for i in reversed(xrange(len(textFile_tweet))):
        response = alchemyapi.sentiment('html', textFile_tweet[i][0].encode('ascii','ignore'))
        if response['status'] == 'OK':
            response['usage'] = ''
            if 'score' in response['docSentiment']:
    	           arb3 = float(unicode(response['docSentiment']['score']))
    	    #print(arb3)
            if textFile_tweet[i][1]==curDate2:
                tweetSum += arb3
                tweetCounter += 1
                #print(tweetCounter)
                tempList.append(arb3)
            else:
                if tweetCounter == 0:
                    tweetCounter == 1;
                tweetAvg = (tweetSum/tweetCounter)*5 + 5
                print(tweetAvg)
                tweetStdError = np.std(tempList)/float(np.sqrt(len(tempList)))
                tempList = []
                if i == len(textFile_tweet)-1:
                    stackTweet.append((tweetAvg,tweetStdError, textFile_tweet[i][1],tweetCounter))
                else:
                    stackTweet.append((tweetAvg,tweetStdError, textFile_tweet[i+1][1],tweetCounter))
                tweetSum = arb3
                tweetCounter = 1
                curDate2 = textFile_tweet[i][1]
            #print(arb3*5+5)
        else:
            print('Error in sentiment analysis call: ', response['statusInfo'])
    tweetAvg = (tweetSum/tweetCounter)*5.0 + 5.0
    print(tweetAvg)
    tweetStdError = np.std(tempList)/float(np.sqrt(len(tempList)))
    tempList = []
    stackTweet.append((tweetAvg,tweetStdError, textFile_tweet[i][1],tweetCounter))
    # for i in xrange(len(stackTweet)):
    #     #print('i = ',i,"out of ",len(stackTweet))
    #     element = stackTweet.pop()
    #     print(element)
    # Format {Rating, StdDev, Date, Counter}
    return stackTweet

def WeightedData (FbData, TwData):
    WData = []
    index = 0
    print('Weighted Data format: Rating, StdErr, Date')
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
    #print(WData)
    return WData

def DecayData (WData):
    DecData = []
    for i in xrange (4, len(WData)):
        maxDecError = max(WData[i][1], WData[i-1][1], WData[i-2][1], WData[i-3][1], WData[i-4][1])
        wAvg = WData[i][0] * 0.6 + WData[i-1][0] * 0.2 + WData[i-2][0] * 0.1 + WData[i-3][0] *0.05 + WData[i-4][0] *0.05
        wErr = maxDecError
        DecData.append((wAvg,wErr))

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
    for i in xrange (0, len(DecData)):
        sum += DecData[i][0]
        print('Sum: ', sum)
    AvgScore = float(sum)/len(DecData)
    return AvgScore
