from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from .clients import TwitterClient


#
#   Search
#   Referenced by images, tweets, and articles.
#
class Search(models.Model):
    search_string = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.search_string


#
#   Image
#   A result from Imgur.
#
class Image(models.Model):
    url = models.CharField(max_length=255)
    search = models.ForeignKey(Search)

    def __str__(self):
        return self.url


#
#   Tweet
#   A result from Twitter.
#
class Tweet(models.Model):
    message = models.TextField()
    username = models.CharField(max_length=255)
    search = models.ForeignKey(Search)
    created_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.username + '\n' + self.message

    def for_display(self):
        return [self.username, self.message]


#
#   Article
#   A result from Wikipedia.
#
class Article(models.Model):
    title = models.CharField(max_length=255)
    summary = models.TextField()
    search = models.ForeignKey(Search)

    def __str__(self):
        return self.title + '\n' + self.summary

    def for_display(self):
        return [self.title, self.summary]


@receiver(post_save, sender=Search)
def do_search(sender, instance, created, **kwargs):
    if created:
        #  Get twitter
        twitter = TwitterClient()
        twitter_results = twitter.search(instance.search_string)
        for tweet in twitter_results:
            new_tweet = Tweet(message=tweet.text, username=tweet.user.name,
                              created_at=tweet.created_at, search=instance)
            new_tweet.save()
