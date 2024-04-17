from django import template
from django.conf import settings
from urllib.parse import urljoin

register = template.Library()

@register.filter
def mediapath(image_url):
    if "no_image" in image_url:
        return urljoin(settings.MEDIA_URL, 'imgs/no_image.png')
    return urljoin(settings.MEDIA_URL, image_url)
