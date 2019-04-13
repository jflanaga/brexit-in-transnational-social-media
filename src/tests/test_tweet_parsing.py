import json
import pytest


import src.data.parse_tweets as parse_tweets
from src.paths import TEST_DATA_DIRECTORY

TEST_DATA = TEST_DATA_DIRECTORY / 'test_tweet.jsonl'

text = "N) A Tweet with explicit geo coordinates https://t.co/XkcFAgHhsj"
url = 'https://twitter.com/briefing4brexit/status/1108796336202231808'
tweet_url = 'https://twitter.com/RobotPrincessFi/status/887453193294282752'
media = "https://twitter.com/RobotPrincessFi/status/887453193294282752/photo/1"


@pytest.fixture
def tweet(file=TEST_DATA):
    with open(file) as f:
        return json.load(f)


def test_text(tweet):
    assert parse_tweets.text(tweet) == text


def test_coordinates(tweet):
    assert parse_tweets.coordinates(tweet) == '-105.277869 40.017365'


def test_place(tweet):
    assert parse_tweets.place(tweet) == 'Boulder, CO'


def test_hashtags(tweet):
    assert parse_tweets.hashtags(tweet) == ''


def test_all_hastags(tweet):
    assert parse_tweets.all_hashtags(tweet) == ''


def test_media(tweet):
    assert parse_tweets.media(tweet) == media


def test_urls(tweet):
    assert parse_tweets.urls(tweet) == ''


def test_retweet_id(tweet):
    assert parse_tweets.retweet_id(tweet) == ''


def test_retweet_screen_name(tweet):
    assert parse_tweets.retweet_screen_name(tweet) == ''


def test_retweet_user_id(tweet):
    assert parse_tweets.retweet_user_id(tweet) == ''


def test_tweet_url(tweet):
    assert parse_tweets.tweet_url(tweet) == tweet_url


def test_user_urls(tweet):
    assert parse_tweets.user_urls(tweet) == ''


def test_tweet_type(tweet):
    assert parse_tweets.tweet_type(tweet) == 'original'


if __name__ == '__main__':
    pytest.cmdline.main()
