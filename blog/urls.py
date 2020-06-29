from django.urls import path, include
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
)
from . import views

# as_view() is used when sending a request to a class-based view as django's URL resolver natively expects
# the request to be sent to a callable function, not a class-based view.
# when you pass a captured value such as <str:username> or <int:pk> to the path, this captured value is also passed
# to the view as a kwarg. This kwarg is accessible through view.kwargs.
urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='blog-about'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('bioinformatics/', views.bioinformatics, name='blog-CV'),
]