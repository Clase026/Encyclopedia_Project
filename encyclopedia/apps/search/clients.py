from django.conf import settings
import tweepy


class TwitterClient:

    def __init__(self):
        self.auth = self.get_auth()
        self.client = tweepy.API(self.auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    def get_auth(self):
        """Authenticates the twitter client using the API key and secret.
        """
        return tweepy.AppAuthHandler(settings.TWITTER_KEY, settings.TWITTER_SECRET)

    def search(self, search_string):
        """Searches for tweets matching the search string, and returns them all.
        """
        tweets = []
        results = self.client.search(q=search_string)
        for tweet in results:
            if len(tweets) < 10:
                if not (hasattr(tweet, 'retweeted_status') or hasattr(tweet, 'quoted_status')):
                    tweets.append(tweet)
            else:
                break
        return tweets
