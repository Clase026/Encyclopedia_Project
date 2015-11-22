from django.views.generic import DetailView, CreateView, ListView
from django.core.urlresolvers import reverse
from .models import Search, Image, Tweet, Article


class SearchCreateView(CreateView):
    model = Search
    fields = ['search_string']
    template_name = 'search.html'

    def get_success_url(self):
        return reverse('search', kwargs={'pk':self.object.pk})


class SearchListView(ListView):
    model = Search
    template_name = 'list.html'


class SearchDetailView(DetailView):
    model = Search
    template_name = 'results.html'

    def get_context_data(self, **kwargs):
        context = super(SearchDetailView, self).get_context_data(**kwargs)
        context['tweets'] = Tweet.objects.filter(search=kwargs['object'])
        context['article'] = Article.objects.filter(search=kwargs['object'])[0]
        context['images'] = Image.objects.filter(search=kwargs['object'])
        return context
