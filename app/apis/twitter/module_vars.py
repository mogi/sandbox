# -*- coding:utf-8 -*-
import os
from django.conf import settings

# consumer
CONSUMER_KEY = settings.CONSUMER_KEY
CONSUMER_SECRET = settings.CONSUMER_SECRET

# base
SERVER = 'api.twitter.com'
URL = 'https://{}'.format(SERVER)

# auth
REQUEST_TOKEN_URL = '{}/oauth/request_token'.format(URL)
ACCESS_TOKEN_URL = '{}/oauth/access_token'.format(URL)
AUTHORIZATION_URL = '{}/oauth/authorize'.format(URL)

# api
STATUSES_UPDATE_URL = "{}/1.1/statuses/update.json".format(URL)


# cache key
OAUTH_TOKEN = "apis.twitter::auth_token_key::key={}"
OAUTH_TOKEN_SECRET = "apis.twitter::auth_token_secret::key={}"
ACCESS_TOKEN_KEY = "apis.twitter::access_token_key::key={}"
ACCESS_TOKEN_SECRET = "apis.twitter::access_token_secret::key={}"
TW_RESPONCE = "apis.twitter::tweet_responce::key={}"
TW_CONTENT = "apis.twitter::tweet_content::key={}"
