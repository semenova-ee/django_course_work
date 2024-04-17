from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from pytils.translit import slugify

from blog.forms import BlogForm
from blog.models import Blog


class BlogCreateView(CreateView):
    model = Blog
    template_name = 'blog/blog_form.html'
    form_class = BlogForm
    success_url = reverse_lazy('blog:list')
    # fields = ['title', 'text', 'image', 'is_published']

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Добавление статьи'
        return context_data


class BlogListView(ListView):
    model = Blog
    template_name = 'blog/blog_list.html'
    # context_object_name = 'posts'

    # def get_queryset(self):
    #     return Blog.objects.filter(is_published=True)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Mailing Service - Blog'
        return context_data

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        return queryset



# class BlogCreateView(PermissionRequiredMixin, CreateView):
#     model = Blog
#     fields = ('title', 'text', 'image', 'is_published')
#     template_name = 'blog/blog_form.html'
#     # form_class = BlogForm
#     permission_required = 'blog.add_blog'
#     success_url = reverse_lazy('blog:list')

    # def form_valid(self, form):
    #     if form.is_valid():
    #         new_blog = form.save()
    #         new_blog.slug = slugify(new_blog.title)
    #         new_blog.save()
    #     return super().form_valid(form)
    #
    # def get_context_data(self, **kwargs):
    #     context_data = super().get_context_data(**kwargs)
    #     context_data['title'] = 'Добавление новости'
    #     return context_data


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog/blog_detail.html'
    # slug_url_kwarg = 'slug'
    # context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = self.object.title
        return context_data

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object
    # def get(self, request, *args, **kwargs):
    #     # Increment views count
    #     post = get_object_or_404(Blog, slug=self.kwargs['slug'])
    #     post.views_count += 1
    #     post.save()
    #     return super().get(request, *args, **kwargs)


class BlogUpdateView(PermissionRequiredMixin, UpdateView):
    model = Blog
    permission_required = 'blog.change_blog'
    success_url = reverse_lazy('blog:list')
    form_class = BlogForm

    # def get_success_url(self):
    #     return reverse_lazy('blog:view', kwargs={'slug': self.object.slug})
    #
    # def form_valid(self, form):
    #     response = super().form_valid(form)
    #     return HttpResponseRedirect(self.get_success_url())


    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Редактирование поста в блоге'
        return context_data

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()
        return super().form_valid(form)


class BlogDeleteView(PermissionRequiredMixin, DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:list')
    permission_required = 'blog.delete_blog'
    template_name = 'blog/blog_confirm_delete.html'
    # slug_url_kwarg = 'slug'
    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Удаление новости'
        return context_data

    # def get_context_data(self, **kwargs):
    #     context_data = super().get_context_data(**kwargs)
    #     context_data['title'] = 'Удаление новости'
    #     # return context_data
    #     context_data['post'] = self.object
    #
    #     # Check the HTTP_REFERER to determine if the request came from post_detail
    #     referer = self.request.META.get('HTTP_REFERER', '')
    #     referer = referer.split("/")
    #     if referer[-2] != 'blog':
    #         context_data['cancel_url'] = reverse('blog:view', kwargs={'slug': self.object.slug})
    #     else:
    #         context_data['cancel_url'] = reverse('blog:list')
    #     return context_data