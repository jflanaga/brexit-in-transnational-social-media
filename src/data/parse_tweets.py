# -- coding: utf-8 --
# adapted from https://github.com/DocNow/twarc/blob/master/twarc/json2csv.py


from typing import Dict
from contextlib import suppress
from src.utils import pluck


def text(t: Dict) -> str:
    """
    Get text of tweet
    """
    return t.get('full_text') or t.get('extended_tweet',
                                       {}).get('full_text') or t['text']


def extended_text(t: Dict) -> str:
    with suppress(KeyError):
        return pluck(t, 'extended_tweet.full_text')

    with suppress(KeyError):
        return pluck(t, 'retweeted_status.extended_tweet.full_text')

    with suppress(KeyError):
        return pluck(t, 'quoted_status.extended_tweet.full_text')

    return ''


def quote(t: Dict) -> str:
    with suppress(KeyError):
        return pluck(t, 'quoted_status.text')
    return ''


def coordinates(t: Dict) -> str:
    """
    Get location coordinates in the form [longitude, latitude] (if available)
    """
    with suppress(TypeError):
        return '%f %f' % tuple(pluck(t, 'coordinates.coordinates'))
    return ''


def place(t: Dict) -> str:
    """
    Full human-readable representation of the place’s name (if available)
    """
    with suppress(TypeError):
        return pluck(t, 'place.full_name')
    return ''


def hashtags(t: Dict) -> str:
    """
    Get all hashtags, including when tweet is truncated (if available)
    """
    # extended tweet
    with suppress(KeyError):
        # noinspection PyTypeChecker
        return ' '.join([
            h['text'] for h in pluck(
                t, 'extended_tweet.entities.hashtags')
        ])
    # standard hashtag field
    return ' '.join(
        [h['text'] for h in t['entities']['hashtags']])


# noinspection PyTypeChecker
def quoted_or_retweeted_hashtags(t: Dict) -> str:
    """
    Get quoted or retweeted hashtags
    """
    # retweets
    with suppress(KeyError):
        return ' '.join([
            h['text']
            for h
            in pluck(t, 'retweeted_status.extended_tweet.entities.hashtags')
        ])

    # quotes
    with suppress(KeyError):
        return ' '.join([
            h['text']
            for h in pluck(t, 'quoted_status.extended_tweet.entities.hashtags')
        ])
    return ''


# noinspection PyTypeChecker
def media(t: Dict) -> str:
    """
    An expanded version of display_url. Links to the media display page
    """
    with suppress(KeyError):
        m = pluck(t, 'extended_entities.media')
        if m:
            return ' '.join([h['expanded_url'] for h in m])
    with suppress(KeyError):
        m = pluck(t, 'entities.media')
        if m:
            return ' '.join([h['expanded_url'] for h in m])
    return ''


def urls(t: Dict) -> str:
    """
    URLs included in the text of a Tweet.
    """
    return ' '.join([h['expanded_url'] or '' for h in t['entities']['urls']])


def retweet_id(t: Dict) -> str:
    """
    integer value Tweet ID of the retweeted or quoted Tweet
    """
    with suppress(KeyError):
        return pluck(t, 'retweeted_status.id_str')

    with suppress(KeyError):
        return pluck(t, 'quoted_status.id_str')
    return ""


def retweet_screen_name(t: Dict) -> str:
    """
    Name of Original Tweeter
    """
    with suppress(KeyError):
        return pluck(t, 'retweeted_status.user.screen_name')
    with suppress(KeyError):
        return pluck(t, 'quoted_status.user.screen_name')
    return ""


def retweet_user_id(t: Dict) -> str:
    """
    Integer value Tweet ID of the Original Tweeter
    """
    with suppress(KeyError):
        return pluck(t, 'retweeted_status.user.id_str')
    with suppress(KeyError):
        return pluck(t, 'quoted_status.user.id_str')
    return ""


def tweet_url(t: Dict) -> str:
    return "https://twitter.com/%s/status/%s" % (t['user']['screen_name'],
                                                 t['id_str'])


def user_urls(t: Dict) -> str:
    """
    url of the Tweeter
    """
    with suppress(KeyError):
        u = pluck(t, 'user.entities.url.urls')
        # noinspection PyTypeChecker,PyTypeChecker
        return " ".join([url[
                             'expanded_url'] for url in u
                         if url['expanded_url']])
    return ""


def tweet_type(t: Dict) -> str:
    """
    Type of tweet (Reply, retweet, quote, original
    """
    if t.get('in_reply_to_status_id'):
        return 'reply'
    if 'retweeted_status' in t:
        return 'retweet'
    if 'quoted_status' in t:
        return 'quote'
    return 'original'
