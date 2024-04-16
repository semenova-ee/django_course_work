from django.db import models
from django.utils.text import slugify


# Create your models here.

class Blog(models.Model):
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    slug = models.CharField(max_length=150, verbose_name='slug',  null=True, blank=True)
    text = models.TextField(verbose_name='Содержимое')
    image = models.ImageField(upload_to='blog', verbose_name='Превью', null=True, blank=True)
    data_created = models.DateField(verbose_name='Дата создания', auto_now=True)
    is_published = models.BooleanField(verbose_name='Опубликовано', default=True)
    views_count = models.IntegerField(default=0, verbose_name='Просмотры')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Generate a slug from the title if not provided
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)