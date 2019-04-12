# -- coding: utf-8 --
# adapted from https://raw.githubusercontent.com/DocNow/twarc/master/twarc/json2csv.py

import csv
import codecs
import gzip
import json

import parse_tweets

from dateutil.parser import parse as date_parse
from pathlib import Path
from typing import Dict, Iterable, List

from src.utils import is_gz_file
from src.paths import RAW_CORPUS, INTERIM_CORPUS
from src.get_logs import logger


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
        parse_tweets.tweet_url(t),
        get('created_at'),
        date_parse(get('created_at')),
        user('screen_name'),
        parse_tweets.text(t),
        parse_tweets.tweet_type(t),
        parse_tweets.coordinates(t),
        parse_tweets.place(t),
        parse_tweets.hashtags(t),
        parse_tweets.media(t),
        parse_tweets.urls(t),
        get('favorite_count'),
        get('in_reply_to_screen_name'),
        get('in_reply_to_status_id'),
        get('in_reply_to_user_id'),
        get('lang'),
        get('possibly_sensitive'),
        get('retweet_count'),
        parse_tweets.retweet_id(t),
        parse_tweets.retweet_screen_name(t),
        parse_tweets.retweet_user_id(t),
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
        parse_tweets.user_urls(t),
        user('verified'),)


def main(src_path: Path, dst_path: Path):
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
            except Exception as e:
                logger.warning(e)
                continue


if __name__ == '__main__':
    main(RAW_CORPUS, INTERIM_CORPUS)
