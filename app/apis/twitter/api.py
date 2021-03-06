# -*- coding:utf-8 -*-
import httplib
from django.core.cache import cache
from django.http import HttpRequest
from oauth2 import (Client,
                    Consumer,
                    Request,
                    Token,
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
    def __init__(self, server,
                 request_token_url='', access_token_url=''):
        self.server = server
        self.request_token_url = request_token_url
        self.access_token_url = access_token_url
        self.connection = httplib.HTTPSConnection(str(self.server))

    def fetch(self, oauth_request, url):
        # via headers
        # -> Token
        self.connection.request(oauth_request.method,
            url, headers=oauth_request.to_header()) 
        response = self.connection.getresponse()
        res = response.read()
        return Token.from_string(res)

    def fetch_request_token(self, oauth_request):
        return self.fetch(oauth_request, self.request_token_url)

    def fetch_access_token(self, oauth_request):
        return self.fetch(oauth_request, self.access_token_url)


def auth(callback_url):
    # setup
    client = SimpleClient(SERVER, REQUEST_TOKEN_URL, ACCESS_TOKEN_URL)
    consumer = Consumer(CONSUMER_KEY, CONSUMER_SECRET)

    # get request token
    oauth_request = Request.from_consumer_and_token(
        consumer, http_method="POST",
        http_url=client.request_token_url,
        parameters={'oauth_callback': callback_url})
    oauth_request.sign_request(SignatureMethod_HMAC_SHA1(),
                               consumer, None)
    token = client.fetch_request_token(oauth_request)
    cache.set('app.root.view.post::oauth_token', token.key, 300)
    cache.set('app.root.view.post::oauth_token_secret', token.secret, 300)

    oauth_request = Request.from_token_and_callback(
                        token=token, http_url=AUTHORIZATION_URL)
    return oauth_request.to_url()

