from django.urls import path
from django.views.decorators.cache import cache_page

from blog.apps import BlogConfig
from blog.views import BlogCreateView, BlogUpdateView, BlogListView, BlogDetailView, BlogDeleteView

app_name = BlogConfig.name

urlpatterns = [
    path('', BlogListView.as_view(), name='list'),
    path('create', BlogCreateView.as_view(), name='create'),
    path('update/<int:pk>', BlogUpdateView.as_view(), name='edit'),
    path('view/<int:pk>', BlogDetailView.as_view(), name='view'),
    path('delete/<int:pk>', BlogDeleteView.as_view(), name='delete'),
    ]