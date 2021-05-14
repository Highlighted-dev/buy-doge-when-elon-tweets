import requests
import json
import os
import time
import secrets
from datetime import datetime
from difflib import SequenceMatcher
from binance_f import RequestClient
from binance_f.constant.test import *
from binance_f.base.printobject import *
from binance_f.model.constant import *


def connect_to_endpoint(url, headers, params):
    response = requests.request("GET", url, headers=headers, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()

#Getting parametrs from tweets
def get_params():
    return {"tweet.fields": "created_at,attachments"}

#Authorization
def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers

def main():
    #twitter setup
    lastDate = datetime.now()
    bearer_token = secrets.bearer_token
    API_key = secrets.API_key
    API_secret_key = secrets.API_secret_key

    #Elon musk twitter url
    url = "https://api.twitter.com/2/users/44196397/tweets"
    headers = create_headers(bearer_token)
    params = get_params()

    bought = False
    while not bought:
        try: 
            json_response = connect_to_endpoint(url, headers, params) #get latest tweets
            tweets = json_response['data']
            print("Search: ")
            for tweet in tweets:
                 
                tweetDate = datetime.strptime(tweet['created_at'][:-1], '%Y-%m-%dT%H:%M:%S.%f') #get the time the tweet was posted
                tweetContent = tweet['text'].lower() 
                splitTweetContent = tweetContent.split() #split tweet into words
                for word in splitTweetContent: #iterate through each word in the tweet
                            if word == "doge" :
                                bought = True
                                cryptoMessage = "Doge found in Elon's tweet: " + tweet['text'] #generate crypto found message
                                print(cryptoMessage)
                                #Remember, that this is posting order on your binance Futures account and will take the multiplier, for example x25, that you have on doge.
                                request_client = RequestClient(api_key=secrets.API_key_binance,secret_key=secrets.API_secret_key_binance,url='https://fapi.binance.com')
                                result = request_client.post_order(symbol="DOGEUSDT", side=OrderSide.BUY, ordertype=OrderType.MARKET, quantity=6100)
                                requests.post(url)
                                
                                break
                if bought:
                    break

            print("Waiting 2 minutes")
            time.sleep(60)
            print("Waiting 60 seconds")
            time.sleep(60)
        except:
            print("Error")
main()
