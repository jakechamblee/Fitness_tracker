from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .models import Post


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html by default
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        # you are passing a dict object as {'username': 'exampleusername'} by the use of self.kwargs
        # this is the captured URL keyword argument, and it comes from the captured value in the URLpath/URLconf
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post


# IMPORTANT: Inherited views MUST come after ALL inherited Mixins due to python's MRO list order.
class PostCreateView(LoginRequiredMixin, CreateView):
    # this view references the post_form.html template. This is also true for the update and delete views.
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        # overriding form_valid() to set the author to the user creating the post
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        # gets the post you are updating. Must return True or access will be denied by UserPassesTestMixin
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        # Must return True or access will be denied by UserPassesTestMixin
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def bioinformatics(request):
    return render(request, 'blog/bioinformatics.html', {'title': 'Bioinformatics'})


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
