from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from .clients import TwitterClient, WikipediaClient, ImgurClient


#
#   Search
#   Referenced by images, tweets, and articles.
#
class Search(models.Model):
    search_string = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return self.search_string


#
#   Image
#   A result from Imgur.
#
class Image(models.Model):
    url = models.CharField(max_length=255)
    title = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)
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

    def __unicode__(self):
        return self.username + '\n' + self.message

    def for_display(self):
        return [self.username, self.message]


#
#   Article
#   A result from Wikipedia.
#
class Article(models.Model):
    title = models.CharField(max_length=255)
    url = models.CharField(max_length=255, null=True)
    summary = models.TextField()
    search = models.ForeignKey(Search)


@receiver(post_save, sender=Search)
def do_search(sender, instance, created, **kwargs):
    if created:
        #  Get twitter
        twitter_results = TwitterClient().search(instance.search_string)
        for tweet in twitter_results:
            new_tweet = Tweet(message=tweet.text, username=tweet.user.name,
                              created_at=tweet.created_at, search=instance)
            new_tweet.save()

        # Get wikipedia
        wiki_result = WikipediaClient().search(instance.search_string)
        new_article = Article(title=wiki_result.title, summary=wiki_result.summary,
                              url=wiki_result.url, search=instance)
        new_article.save()

        # Get imgur
        imgur_results = ImgurClient().search(instance.search_string)
        for image in imgur_results:
            new_image = Image(title=image.title, url=image.link,
                              description=image.description, search=instance)
            new_image.save()
