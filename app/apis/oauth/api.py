# -*- coding:utf-8 -*-
import httplib
from django.http import HttpRequest
from oauth2 import (Client,
                    Consumer,
                    Request,
                    Token,
                    SignatureMethod_HMAC_SHA1)


class SimpleClient(Client):
    """
    oauth client using httplib with headers
    """
    def __init__(self, server, request_token_url,
                 access_token_url, authorization_url,
                 consumer_key, consumer_secret):
        self.server = server
        self.request_token_url = request_token_url
        self.access_token_url = access_token_url
        self.authorization_url = authorization_url
        self.consumer = Consumer(consumer_key, consumer_secret)
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


    def get_auth_url(self, callback_url):
        # get request token
        oauth_request = Request.from_consumer_and_token(
            self.consumer, http_method="POST",
            http_url=self.request_token_url,
            parameters={'oauth_callback': callback_url})
        oauth_request.sign_request(SignatureMethod_HMAC_SHA1(),
                                   self.consumer, None)
        token = self.fetch_request_token(oauth_request)
        # get authorization url
        oauth_request = Request.from_token_and_callback(
                            token=token, http_url=self.authorization_url)
        return oauth_request.to_url(), token

    def get_access_token(self, key, secret, verifier):
        token = Token(key, secret)
        token.set_verifier(verifier)
        oauth_request = Request.from_consumer_and_token(
            self.consumer, http_method="POST", token=token,
            http_url=self.request_token_url)
        oauth_request.sign_request(SignatureMethod_HMAC_SHA1(),
                                   self.consumer, None)
        return self.fetch_access_token(oauth_request)
