from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import render
from .filters import NewsFilter
from .models import Post
from .forms import PostForm
from django.urls import reverse_lazy

class NewsList(ListView):
    model = Post
    ordering = 'created'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10

class SearchList(ListView):
    model = Post
    ordering = 'created'
    template_name = 'search.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):

        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

class NewsDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'

class PostCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'editpost.html'

class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'editpost.html'

class PostDelete(DeleteView):
    model = Post
    template_name = 'deletepost.html'
    success_url = reverse_lazy('post_list')

def index(request):
    return render(request, 'index.html')