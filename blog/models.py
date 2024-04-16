from django.db import models
from django.utils.text import slugify


class BlogPost(models.Model):
    title = models.CharField(max_length=50)
    slug = models.CharField(max_length=255, unique=True, blank=True, null=True)
    content = models.TextField()
    preview = models.ImageField(upload_to="blog_imgs", blank=True)
    created_at = models.DateField(auto_now_add=True, blank=True)
    is_published =  models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Generate a slug from the title if not provided
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

        class Meta:
            verbose_name = 'Статья'
            verbose_name_plural = 'Статьи'