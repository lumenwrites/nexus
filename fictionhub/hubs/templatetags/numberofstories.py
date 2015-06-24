# markdownify
from django import template
from hubs.models import Hub

register = template.Library()

@register.simple_tag(takes_context=True)
def numberofstories(context, hub):
    request = context['request']
    rational = False
    if request.META['HTTP_HOST'] == "rationalfiction.io":
        rational = True

    stories = hub.posts.filter(published = True, rational=rational) # , rational = True
    number = stories.count()
    return number
 
