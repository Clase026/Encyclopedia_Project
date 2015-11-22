from django.conf.urls import url
from .views import SearchCreateView, SearchDetailView

urlpatterns = [
    url(r'$', SearchCreateView.as_view(), name='new_search'),
    url(r'search/(?P<pk>\d+)$', SearchDetailView.as_view(), name='search')
]