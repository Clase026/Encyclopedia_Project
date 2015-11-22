from django.db import models


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
