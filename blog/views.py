from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from pytils.translit import slugify

from blog.models import Blog


class BlogCreateView(PermissionRequiredMixin, CreateView):
    model = Blog
    fields = ('title', 'text', 'image', 'is_published')
    permission_required = 'blog.add_blog'

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Добавление новости'
        return context_data

    def get_success_url(self):
        return reverse_lazy('blog:list')


class BlogListView(ListView):
    model = Blog

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Новости'
        return context_data

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        return queryset


class BlogDetailView(DetailView):
    """Контроллер просмотра отдельной новости"""
    model = Blog

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = self.object.title
        return context_data

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class BlogUpdateView(PermissionRequiredMixin, UpdateView):
    model = Blog
    fields = ('title', 'text', 'image', 'is_published')
    permission_required = 'blog.change_blog'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Редактирование новости'
        return context_data

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog:list')


class BlogDeleteView(PermissionRequiredMixin, DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:list')
    permission_required = 'blog.delete_blog'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Удаление новости'
        return context_data