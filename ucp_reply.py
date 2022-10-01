# -*- coding: utf-8 -*-
import tweepy
from datetime import timedelta

import base64
import hashlib
import hmac
import json
import os

from flask import Flask, request, abort
from ucp_twitter_bot import twitter_authentication

api = twitter_authentication.set_authetication()
TWITTER_CONSUMER_SECRET=os.getenv('CONSUMER_SECRET')

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "hello world!"

# Defines a route for the GET request
@app.route('/webhooks/twitter', methods=['GET'])
def webhook_challenge():
    if 'crc_token' in request.args and len(request.args.get('crc_token')) == 48:
        crc_token = request.args.get('crc_token')
        print("Twitter Consumer Secret : " , TWITTER_CONSUMER_SECRET)
        # creates HMAC SHA-256 hash from incomming token and your consumer secret
        sha256_hash_digest = hmac.new(TWITTER_CONSUMER_SECRET.encode(),
                                        msg=crc_token.encode(), 
                                        digestmod=hashlib.sha256).digest()

        # construct response data with base64 encoded hash
        response = {
            'response_token': 'sha256=' + base64.b64encode(sha256_hash_digest)
        }
        # returns properly formatted json response
        return (json.dumps(response), 200, {'Content-Type': 'application/json'} )
    return ('No Content', 204, {'Content-Type': 'text/plain'})

@app.route('/webhooks/twitter', methods=['POST'])
def get_twitterpost():
    print (request.headers)
    print ("body: %s" % request.get_data())
    return (request.get_data())


if __name__ == "__main__":
    #app.run()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port = port)
    #app.run(host=["199.59.148.0/22","199.16.156.0/22"])