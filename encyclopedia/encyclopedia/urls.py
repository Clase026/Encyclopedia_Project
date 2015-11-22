"""encyclopedia URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from apps.search.views import SearchCreateView, SearchDetailView, SearchListView

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', SearchCreateView.as_view(), name='new_search'),
    url(r'^search/$', SearchListView.as_view(), name='search_list'),
    url(r'^search/(?P<pk>\d+)$', SearchDetailView.as_view(), name='search')
]
