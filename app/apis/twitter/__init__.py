# -*- coding:utf-8 -*-
"""
methods to use twitter api
"""
import module_vars as V
from django.core.cache import cache
from oauth2 import Client, Consumer, Token
from app.apis.oauth import SimpleClient


def get_cache_tw_result(auth_key):
    """
    get cached value, after make cache key.
    >>> get_cache_tw_result("test_auth_key")
    "responce", "authorize key"

    :param auth_key: twitter authorize key
    :type auth_key: str
    :returns: chaced string
    :rtype: str, str
    """
    return cache.get(V.TW_RESPONCE.format(auth_key)), cache.get(V.TW_CONTENT.format(auth_key))


def get_cache_auth_secret(auth_key):
    """
    get cached value, after make cache key.
    >>> get_cache_auth_secret("test_auth_key")
    "secret"

    :param auth_key: twitter authorize key
    :type auth_key: str
    :returns: auth_token_secret retruned by twitter
    :rtype: str
    """
    key = V.OAUTH_TOKEN_SECRET
    return cache.get(key.format(auth_key))


def delete_cache(auth_key):
    """
    delete chace by auth_key
    >>> delete_cache("test_auth_key")

    :param auth_key: twitter authorize key
    :type auth_key: str
    """
    cache.delete_many([
        V.OAUTH_TOKEN.format(auth_key),
        V.OAUTH_TOKEN_SECRET.format(auth_key),
        V.ACCESS_TOKEN_KEY.format(auth_key),
        V.ACCESS_TOKEN_SECRET.format(auth_key),
        V.TW_RESPONCE.format(auth_key),
        V.TW_CONTENT.format(auth_key),
    ])


def set_cache(auth_key, key, value):
    """
    set cache value, after make cache key, 
    >>> set_cache("test_auth_key")

    :param auth_key: twitter authorize key
    :type auth_key: str
    :param key: cache key
    :type key: str
    :param value: cache value
    :type key: str
    """
    cache.set(key.format(auth_key), value, 300)


def auth(callback_url):
    """
    get url to twitter and cache returnd key and secret.
    >>> auth("http://127.0.0.1:8000")

    :param callback_url
    :type str
    :returns: url to twitter
    :rtype: str
    """
    client = SimpleClient(V.SERVER,
                          V.REQUEST_TOKEN_URL,
                          V.ACCESS_TOKEN_URL, V.AUTHORIZATION_URL,
                          V.CONSUMER_KEY, V.CONSUMER_SECRET)
    url, token = client.get_auth_url(callback_url)

    set_cache(token.key, V.OAUTH_TOKEN, token.key)
    set_cache(token.key, V.OAUTH_TOKEN_SECRET, token.secret)
    return url


def tweet_with_auth(message, key, secret, verifier):
    """
    get access key and call twitter api.
    >>> tweet_with_auth("hello", "key", "secret", "verifier")

    :param message: message to tweet
    :type key: str
    :param key:
    :type key: str
    :param secret:
    :type key: str
    :param verifier :
    :type key: str
    :returns: result call api
    :rtype: dict, dict
    """
    client = SimpleClient(V.SERVER,
                          V.REQUEST_TOKEN_URL,
                          V.ACCESS_TOKEN_URL, V.AUTHORIZATION_URL,
                          V.CONSUMER_KEY, V.CONSUMER_SECRET)
    token = client.get_access_token(key, secret, verifier)
    set_cache(key, V.ACCESS_TOKEN_KEY, token.key)
    set_cache(key, V.ACCESS_TOKEN_SECRET, token.secret)
    return tweet(message, token.key, token.secret, key)


def tweet(message, key, secret, auth_key):
    """
    get access key and call twitter api.
    >>> tweet_with_auth("hello", "key", "secret", "verifier")

    :param message: message to tweet
    :type key: str
    :param key:
    :type key: str
    :param secret:
    :type key: str
    :param auth_key: authorize key
    :type key: str
    :returns: result call api
    :rtype: dict, dict
    """
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
