from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import BlogPost
from .forms import BlogPostForm


class BlogPostListView(ListView):
    model = BlogPost
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Новости'
        return context_data

    def get_queryset(self):
        return BlogPost.objects.filter(is_published=True)


class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    slug_url_kwarg = 'slug'

    def get(self, request, *args, **kwargs):
        # Increment views count
        post = get_object_or_404(BlogPost, slug=self.kwargs['slug'])
        post.views += 1
        post.save()
        return super().get(request, *args, **kwargs)



class BlogPostCreateView(CreateView):
    model = BlogPost
    template_name = 'blog/post_form.html'
    form_class = BlogPostForm
    success_url = reverse_lazy('blog:post_list')


class BlogPostUpdateView(UpdateView):
    model = BlogPost
    template_name = 'blog/post_form.html'
    form_class = BlogPostForm
    slug_url_kwarg = 'slug'

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'slug': self.object.slug})

    def form_valid(self, form):
        response = super().form_valid(form)
        return HttpResponseRedirect(self.get_success_url())


class BlogPostDeleteView(DeleteView):
    model = BlogPost
    template_name = 'blog/post_confirm_delete.html'
    slug_url_kwarg = 'slug'
    success_url = reverse_lazy('blog:post_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = self.object

        # Check the HTTP_REFERER to determine if the request came from post_detail
        referer = self.request.META.get('HTTP_REFERER', '')
        referer = referer.split("/")
        if referer[-2] != 'blog':
            context['cancel_url'] = reverse('blog:post_detail', kwargs={'slug': self.object.slug})
        else:
            context['cancel_url'] = reverse('blog:post_list')
        return context
