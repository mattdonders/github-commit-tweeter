import os

import tweepy


def send_tweet(testing: bool, msg: str):
    """ Sends out a tweet for a given Github commit (with link).

    Args:
        msg: Github commit message.

    Returns:
        True if tweet sent or TweepyError if failed
    """

    # Get keys from environment variables based on if this is a "test-run" or not.
    if testing:
        consumer_key = os.environ.get("DEBUG_TWTR_CONSUMER_KEY")
        consumer_secret = os.environ.get("DEBUG_TWTR_CONSUMER_SECRET")
        access_token = os.environ.get("DEBUG_TWTR_ACCESS_TOKEN")
        access_secret = os.environ.get("DEBUG_TWTR_ACCESS_SECRET")
    else:
        consumer_key = os.environ.get("TWTR_CONSUMER_KEY")
        consumer_secret = os.environ.get("TWTR_CONSUMER_SECRET")
        access_token = os.environ.get("TWTR_ACCESS_TOKEN")
        access_secret = os.environ.get("TWTR_ACCESS_SECRET")

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)
    try:
        if api.update_status(status=msg):
            return True
    except tweepy.error.TweepError as e:
        return e


def lambda_handler(event, context):
    req_headers = event.get("headers")
    user_agent = req_headers.get("User-Agent")
    github_event = req_headers.get("X-GitHub-Event")

    print(req_headers)
    print(user_agent)
    print(github_event)

    # Enables testing via non-Github sources or Test Payloads
    testing = False if "GitHub-Hookshot" in user_agent else True

    print(f"Testing: {testing}")

    # Gets commits object from Github PUSH Payload
    commits = event.get("body").get("commits")
    print(commits)

    for commit in commits:
        msg = commit.get("message")
        url = commit.get("url")
        tweet_msg = f"🛎 New Gamebot Feature: {msg}\n\n{url}"
        send_tweet(testing, tweet_msg)

    # Generate a smaller commits response
    commit_resp = [x.get("message") for x in commits]
    print(commit_resp)

    return {"statusCode": 200, "commits": commit_resp, "testing": testing}

