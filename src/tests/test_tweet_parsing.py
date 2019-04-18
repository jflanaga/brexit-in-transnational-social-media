import json
import pytest

import src.data.parse_tweets as parse_tweets
from src.paths import TEST_DATA_DIRECTORY

TEST_DATA = TEST_DATA_DIRECTORY / 'test_cases.jsonl'

lines = TEST_DATA.read_text().split('\n')


expected_text = [
    "N) A Tweet with explicit geo coordinates https://t.co/XkcFAgHhsj",
    "N) A Tweet tagged with a Twitter place. https://t.co/rspQ5CZUfX",
    "M) This is a #QuoteTweet with #hashtags! https://t.co/rw4TMg9O5k",
    "L) This is a #Tweet with a #hashtag"
]
expected_tags = ['', '', "QuoteTweet hashtags", "Tweet hashtag"]
expected_coords = ['-105.277869 40.017365', '']
expected_places = ['Boulder, CO', 'Boulder, CO', '']
expected_media = [
    "https://twitter.com/RobotPrincessFi/status/887453193294282752/photo/1",
    "https://twitter.com/RobotPrincessFi/status/887450119146270723/photo/1",
    "",
                ]
expected_quoted_id = ["", "", "872836379595620353"]
expected_quoted_screen_name = ["", "", "RobotPrincessFi"]
expected_quoted_user_id = ["", "", "815279070241955840"]
expected_tweet_url = [
    "https://twitter.com/RobotPrincessFi/status/887453193294282752",
    "https://twitter.com/RobotPrincessFi/status/887450119146270723",
    "https://twitter.com/RobotPrincessFi/status/872836479608733696"]


@pytest.fixture
def tweet(request):
    line = request.param
    return json.loads(line)


class TestText:
    @pytest.mark.parametrize('tweet, text',
                             zip(lines, expected_text),
                             ids=tuple(
                                 repr(tag) for tag in expected_text),
                             indirect=('tweet',))
    def test_text(self, tweet, text):
        assert parse_tweets.text(tweet) == text


class TestCoordinates:
    @pytest.mark.parametrize('tweet, coords',
                             zip(lines, expected_coords),
                             ids=tuple(
                                repr(coords) for coords in expected_coords
                                ),
                             indirect=('tweet',))
    def test_coordinates(self, tweet, coords):
        assert parse_tweets.coordinates(tweet) == coords


class TestHashtag:
    @pytest.mark.parametrize('tweet, tag',
                             zip(lines, expected_tags),
                             ids=tuple(repr(tag) for tag in expected_tags),
                             indirect=('tweet',))
    def test_hashtag(self, tweet, tag):
        assert parse_tweets.hashtags(tweet) == tag


class TestPlaces:
    @pytest.mark.parametrize('tweet, place',
                             zip(lines, expected_places),
                             ids=tuple(
                                 repr(place) for place in expected_places
                             ),
                             indirect=('tweet',))
    def test_place(self, tweet, place):
        assert parse_tweets.place(tweet) == place


class TestMedia:
    @pytest.mark.parametrize('tweet, media',
                             zip(lines, expected_media),
                             ids=tuple(
                                 repr(media) for media in expected_media
                             ),
                             indirect=('tweet',))
    def test_media(self, tweet, media):
        assert parse_tweets.media(tweet) == media


class TestQuotedId:
    @pytest.mark.parametrize('tweet, quoted_id',
                             zip(lines, expected_quoted_id),
                             ids=tuple(repr(id) for id in expected_quoted_id),
                             indirect=('tweet',))
    def test_quoted_id(self, tweet, quoted_id):
        assert parse_tweets.retweet_id(tweet) == quoted_id


class TestQuotedScreenName:
    @pytest.mark.parametrize('tweet, quoted_screen_name',
                             zip(lines, expected_quoted_screen_name),
                             ids=tuple(
                                 repr(screen_name)
                                 for screen_name in expected_quoted_screen_name
                             ),
                             indirect=('tweet',))
    def test_quoted_screen_name(self, tweet, quoted_screen_name):
        assert parse_tweets.retweet_screen_name(tweet) == quoted_screen_name


class TestQuotedUserId:
    @pytest.mark.parametrize('tweet, quoted_user_id',
                             zip(lines, expected_quoted_user_id),
                             ids=tuple(
                                 repr(id) for id in expected_quoted_user_id),
                             indirect=('tweet',))
    def test_quoted_user_id(self, tweet, quoted_user_id):
        assert parse_tweets.retweet_user_id(tweet) == quoted_user_id


class TestTweetUrl:
    @pytest.mark.parametrize('tweet, tweet_url',
                             zip(lines, expected_tweet_url),
                             ids=tuple(
                                 repr(url) for url in expected_tweet_url),
                             indirect=('tweet',))
    def test_user_url(self, tweet, tweet_url):
        assert parse_tweets.tweet_url(tweet) == tweet_url
