# -- coding: utf-8 --
# adapted from https://raw.githubusercontent.com/DocNow/twarc/master/twarc/json2csv.py

import csv
import codecs
import gzip
import json

from dateutil.parser import parse as date_parse
from pathlib import Path
from typing import Dict, Iterable, List, Union

from src.utils import recursive_get, is_gz_file
from src.paths import RAW_CORPUS, INTERIM_CORPUS


def get_headings() -> List[str]:
    """
    Names of header columns
    """
    return [
        'id',
        'tweet_url',
        'created_at',
        'parsed_created_at',
        'user_screen_name',
        'text',
        'extended_tweet',
        'tweet_type',
        'coordinates',
        'place',
        'hashtags',
        'media',
        'urls',
        'favorite_count',
        'in_reply_to_screen_name',
        'in_reply_to_status_id',
        'in_reply_to_user_id',
        'lang',
        'possibly_sensitive',
        'retweet_count',
        'retweet_or_quote_id',
        'retweet_or_quote_screen_name',
        'retweet_or_quote_user_id',
        'source',
        'user_id',
        'user_created_at',
        'user_default_profile_image',
        'user_description',
        'user_favourites_count',
        'user_followers_count',
        'user_friends_count',
        'user_listed_count',
        'user_location',
        'user_name',
        'user_statuses_count',
        'user_time_zone',
        'user_urls',
        'user_verified',
    ]


def get_row(t: Dict) -> Iterable:
    """
    Apply functions to parse tweet
    """
    get = t.get
    user = t.get('user').get
    return (
        get('id_str'),
        tweet_url(t),
        get('created_at'),
        date_parse(get('created_at')),
        user('screen_name'),
        text(t),
        tweet_type(t),
        coordinates(t),
        place(t),
        hashtags(t),
        media(t),
        urls(t),
        get('favorite_count'),
        get('in_reply_to_screen_name'),
        get('in_reply_to_status_id'),
        get('in_reply_to_user_id'),
        get('lang'),
        get('possibly_sensitive'),
        get('retweet_count'),
        retweet_id(t),
        retweet_screen_name(t),
        retweet_user_id(t),
        get('source'),
        user('id_str'),
        user('created_at'),
        user('default_profile_image'),
        user('description'),
        user('favourites_count'),
        user('followers_count'),
        user('friends_count'),
        user('listed_count'),
        user('location'),
        user('name'),
        user('statuses_count'),
        user('time_zone'),
        user_urls(t),
        user('verified'),)


def text(t: Dict) -> str:
    """
    Get text of tweet
    """
    return t.get('full_text') or t.get('extended_tweet',
                                       {}).get('full_text') or t['text']


def coordinates(t: Dict) -> Union[str, None]:
    """
    Get location coordinates in the form [longitude, latitude] (if available)
    """
    try:
        return '%f %f' % tuple(recursive_get(t, 'coordinates', 'coordinates'))
    except AttributeError:
        return None


def place(t: Dict) -> Union[str, None]:
    """
    Full human-readable representation of the place’s name (if available)
    """
    try:
        return recursive_get(t, 'place', 'full_name')
    except AttributeError:
        return None


def hashtags(t: Dict) -> str:
    """
    Get hashtags found in body of tweet, minus # sign
    """
    return ' '.join([h['text'] for h in t['entities']['hashtags']])


# noinspection PyTypeChecker
def media(t: Dict) -> Union[str, None]:
    """
    An expanded version of display_url. Links to the media display page
    """
    m = recursive_get(t, 'entities', 'media')
    if m:
        return ' '.join([h['expanded_url'] for h in m])
    else:
        m = recursive_get(t, 'entities', 'media')
        if m:
            return ' '.join([h['expanded_url'] for h in t])
        else:
            return None


def urls(t: Dict) -> str:
    """
    URLs included in the text of a Tweet.
    """
    return ' '.join([h['expanded_url'] or '' for h in t['entities']['urls']])


def retweet_id(t: Dict) -> Union[str, None]:
    """
    integer value Tweet ID of the retweeted or quoted Tweet
    """
    try:
        return recursive_get(t, 'retweeted_status', 'id_str')
    except AttributeError:
        pass
    try:
        return recursive_get(t, 'quoted_status', 'id_str')
    except AttributeError:
        return None


def retweet_screen_name(t: Dict) -> Union[str, None]:
    """
    Name of Original Tweeter
    """
    try:
        return recursive_get(t, 'retweeted_status', 'user', 'screen_name')
    except AttributeError:
        pass

    try:
        return recursive_get(t, 'quoted_status', 'user', 'screen_name')
    except AttributeError:
        return None


def retweet_user_id(t: Dict) -> Union[str, None]:
    """
    Integer value Tweet ID of the Original Tweeter
    """
    try:
        return recursive_get(t, 'retweeted_status', 'user', 'id_str')
    except AttributeError:
        pass

    try:
        return recursive_get(t, 'quoted_status', 'user', 'id_str')
    except AttributeError:
        return None


def tweet_url(t: Dict) -> str:
    return "https://twitter.com/%s/status/%s" % (t['user']['screen_name'],
                                                 t['id_str'])


def user_urls(t: Dict) -> Union[str, None]:
    """
    url of the Tweeter
    """
    try:
        u = recursive_get(t, 'user', 'entities', 'url', 'urls')
        # noinspection PyTypeChecker,PyTypeChecker
        return " ".join([url['expanded_url'] for url in u if url['expanded_url']])
    except AttributeError:
        return None


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


def parse_tarred_json(src_path: Path, dst_path: Path):
    """
    Parses a directory of tweets of tarred json files
    and writes csv files with same base name to new directory
    """
    for filename in src_path.iterdir():
        if is_gz_file(filename):
            try:
                dst_filename = filename.stem.split('.')[0] + '.csv'
                dst_filepath = dst_path / dst_filename
                with codecs.open(dst_filepath, 'wb', 'utf-8') as dst_file:
                    writer = csv.writer(dst_file)
                    writer.writerow(get_headings())
                    with gzip.open(filename, 'rt', encoding='utf-8') as lines:
                        for line in lines:
                            tweet = json.loads(line)
                            writer.writerow(get_row(tweet))
            except EOFError:
                continue


if __name__ == '__main__':
    parse_tarred_json(RAW_CORPUS, INTERIM_CORPUS)
