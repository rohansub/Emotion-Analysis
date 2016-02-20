from __future__ import print_function
import json
import unicodedata
from alchemyapi import AlchemyAPI

textFile_msg = ["Happy Bunnies!", "I hate life", "I love life"]
textFile_post = ["I am okay", "I am not okay", "Hey guys!"]
textFile_like = ["Hey how are you?", "I hate him", "This is the best!"]
alchemyapi = AlchemyAPI()

# code for fetching text to arrays

messageSum = 0;
postSum = 0;
likeSum = 0;

for i in xrange(len(textFile_msg)):
    response = alchemyapi.sentiment('html', textFile_msg[i])
    if response['status'] == 'OK':
        response['usage'] = ''
        if 'score' in response['docSentiment']:
	    arb1 = float(unicode(response['docSentiment']['score']))
	    print(arb1)	
	    messageSum += arb1         
    else:
        print('Error in sentiment analysis call: ', response['statusInfo'])
msgAvg = (messageSum/len(textFile_msg))*5 + 5

for i in xrange(len(textFile_post)):
    response = alchemyapi.sentiment('html', textFile_post[i])
    if response['status'] == 'OK':
        response['usage'] = ''
        if 'score' in response['docSentiment']:
	    arb2 = float(unicode(response['docSentiment']['score']))
	    print(arb2)
	    postSum += arb2         
    else:
        print('Error in sentiment analysis call: ', response['statusInfo'])
postAvg = (postSum/len(textFile_post))*5 + 5

for i in xrange(len(textFile_like)):
    response = alchemyapi.sentiment('html', textFile_like[i])
    if response['status'] == 'OK':
        response['usage'] = ''
        if 'score' in response['docSentiment']:
	    arb3 = float(unicode(response['docSentiment']['score']))
	    print(arb3)
	    likeSum += arb3         
    else:
        print('Error in sentiment analysis call: ', response['statusInfo'])
likeAvg = (likeSum/len(textFile_like))*5 + 5

print(msgAvg , ', ' , postAvg , ', ' , likeAvg , '.')

weightedSum = 0.75*msgAvg + 0.2*postAvg + 0.05*likeAvg
print(weightedSum)





