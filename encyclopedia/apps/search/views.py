from django.views.generic import DetailView, CreateView
from django.core.urlresolvers import reverse
from .models import Search, Image, Tweet, Article


class SearchCreateView(CreateView):
    model = Search
    fields = ['search_string']
    template_name = 'search.html'

    def get_success_url(self):
        return reverse('search', kwargs={'pk':self.object.pk})


class SearchDetailView(DetailView):
    model = Search
    template_name = 'results.html'
