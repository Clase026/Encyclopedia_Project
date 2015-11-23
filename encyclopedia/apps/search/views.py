from django.views.generic import DetailView, CreateView, ListView
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from .models import Search, Image, Tweet, Article
import datetime


class SearchCreateView(CreateView):
    """Allows the user to execute a search. Creates a new object if the search hasn't been done before."""
    model = Search
    fields = ['search_string']
    template_name = 'search.html'

    def get_success_url(self):
        """Redirect to the search results page."""
        return reverse('search', kwargs={'pk':self.object.pk})

    def form_invalid(self, form):
        """Usually triggers because a term has already been searched for. Attempt to find it. If the search is old,
        ignore this warning and make a new search anyway."""
        searches = Search.objects.filter(search_string=form.data['search_string'])
        if len(searches) > 0:
            search = searches[0]
            if search.date < datetime.date.today():
                search.delete()
                search = Search(search_string=form.data['search_string'])
                search.save()
            return redirect('search', pk=search.id)
        else:
            return redirect('new_search')


class SearchListView(ListView):
    """Displays all searches."""
    model = Search
    template_name = 'list.html'

    def get_context_data(self, **kwargs):
        context = super(SearchListView, self).get_context_data(**kwargs)
        context['today'] = datetime.date.today()
        context['object_list'] = Search.objects.filter(date=context['today'])
        return context


class SearchDetailView(DetailView):
    """Displays results for a search."""
    model = Search
    template_name = 'results.html'

    def get_context_data(self, **kwargs):
        context = super(SearchDetailView, self).get_context_data(**kwargs)
        context['tweets'] = Tweet.objects.filter(search=kwargs['object'])
        context['article'] = Article.objects.filter(search=kwargs['object'])[0]
        context['images'] = Image.objects.filter(search=kwargs['object'])
        return context
