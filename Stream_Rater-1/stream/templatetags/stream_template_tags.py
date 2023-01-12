from django import template
from stream.models import Category, Streamer

register = template.Library()


@register.inclusion_tag('stream/cats.html')
def get_category_list(cat=None):
    return {'cats': Category.objects.all(),
            'streamers': Streamer.objects.all(),
            'act_cat': cat}
