# -*- coding:utf-8 -*-
import httplib
from django.http import HttpRequest
from oauth2 import (Client,
                    Token,
                    Request,
                    Consumer,
                    SignatureMethod_HMAC_SHA1)

SERVER = 'api.twitter.com'
REQUEST_TOKEN_URL = 'https://{}/oauth/request_token'.format(SERVER)
ACCESS_TOKEN_URL = 'https://{}/oauth/access_token'.format(SERVER)
AUTHORIZATION_URL = 'https://{}/oauth/authorize'.format(SERVER)

CONSUMER_KEY = 'SSDm1UIb7JcZJFsLhqDqaoBaV'
CONSUMER_SECRET = '0lE1TdPrL7ve2Je1PnmyRMNG1aaQTl3ft2G7BgxR0suEsWVvIL'

class SimpleClient(Client):
    """
    oauth client using httplib with headers
    """
    def __init__(self, server, request_token_url='',
                 access_token_url='', authorization_url=''):
        self.server = server
        self.request_token_url = request_token_url
        self.access_token_url = access_token_url
        self.authorization_url = authorization_url
        self.connection = httplib.HTTPSConnection(str(self.server))

    def fetch_request_token(self, oauth_request):
        # via headers
        # -> Token
        self.connection.request(oauth_request.method,
            self.request_token_url, headers=oauth_request.to_header()) 
        response = self.connection.getresponse()
        return Token.from_string(response.read())

    def fetch_access_token(self, oauth_request):
        # via headers
        # -> Token
        self.connection.request(oauth_request.method,
            self.access_token_url, headers=oauth_request.to_header()) 
        response = self.connection.getresponse()
        return Token.from_string(response.read())

    def authorize_token(self, oauth_request):
        # via url
        # -> typically just some okay response
        self.connection.request(oauth_request.method,
            oauth_request.to_url()) 
        response = self.connection.getresponse()
        return response.read()


def auth(callback_url):
    # setup
    client = SimpleClient(SERVER, REQUEST_TOKEN_URL,
                          ACCESS_TOKEN_URL, AUTHORIZATION_URL)
    consumer = Consumer(CONSUMER_KEY, CONSUMER_SECRET)

    # get request token
    oauth_request = Request.from_consumer_and_token(
        consumer, http_method="POST",
        http_url=client.request_token_url,
        parameters={'oauth_callback': callback_url})
    oauth_request.sign_request(SignatureMethod_HMAC_SHA1(),
                               consumer, None)
    token = client.fetch_request_token(oauth_request)
    oauth_request = Request.from_token_and_callback(
                        token=token, http_url=client.authorization_url)
    return oauth_request.to_url()
