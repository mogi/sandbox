# -*- coding:utf-8 -*-
import module_vars as V
from django.core.cache import cache
from oauth2 import Client, Consumer, Token
from app.apis.oauth import SimpleClient


def get_cache_access_token_info():
    return cache.get(V.ACCESS_TOKEN_KEY), cache.get(V.ACCESS_TOKEN_SECRET)


def get_cache_tw_result(auth_key):
    return cache.get(V.TW_RESPONCE.format(auth_key)), cache.get(V.TW_CONTENT.format(auth_key))


def get_cache_auth_secret(auth_key):
    key = V.OAUTH_TOKEN_SECRET
    return cache.get(key.format(auth_key))


def delete_cache(auth_key):
    cache.delete_many([
        V.OAUTH_TOKEN.format(auth_key),
        V.OAUTH_TOKEN_SECRET.format(auth_key),
        V.ACCESS_TOKEN_KEY.format(auth_key),
        V.ACCESS_TOKEN_SECRET.format(auth_key),
        V.TW_RESPONCE.format(auth_key),
        V.TW_CONTENT.format(auth_key),
    ])


def set_cache(auth_key, key, value):
    print key.format(auth_key), value
    cache.set(key.format(auth_key), value, 300)


def auth(callback_url):
    client = SimpleClient(V.SERVER,
                          V.REQUEST_TOKEN_URL,
                          V.ACCESS_TOKEN_URL, V.AUTHORIZATION_URL,
                          V.CONSUMER_KEY, V.CONSUMER_SECRET)
    url, token = client.get_auth_url(callback_url)

    set_cache(token.key, V.OAUTH_TOKEN, token.key)
    set_cache(token.key, V.OAUTH_TOKEN_SECRET, token.secret)
    return url


def tweet_with_auth(message, key, secret, verifier):
    client = SimpleClient(V.SERVER,
                          V.REQUEST_TOKEN_URL,
                          V.ACCESS_TOKEN_URL, V.AUTHORIZATION_URL,
                          V.CONSUMER_KEY, V.CONSUMER_SECRET)
    token = client.get_access_token(key, secret, verifier)
    set_cache(key, V.ACCESS_TOKEN_KEY, token.key)
    set_cache(key, V.ACCESS_TOKEN_SECRET, token.secret)
    return tweet(message, token.key, token.secret, key)


def tweet(message, key, secret, auth_key):
    post_body = "status={}".format(message)
    # tweet
    client = Client(Consumer(V.CONSUMER_KEY, V.CONSUMER_SECRET),
                    Token(key, secret))
    res, content = client.request(V.STATUSES_UPDATE_URL,
                                  method="POST",
                                  body=post_body )
    set_cache(auth_key, V.TW_RESPONCE, res)
    set_cache(auth_key, V.TW_CONTENT, content)
    return res, content
