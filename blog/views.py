from django.views.generic import ListView, DetailView, TemplateView
from django.core.paginator import Paginator
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin

class BlogList(ListView):
    paginate_by = 3
    model = Post
    template_name = 'home.html'


class BlogDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'


class AboutPageView(TemplateView):
    template_name = 'about.html'

