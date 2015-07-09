# markdownify
from django import template
from hubs.models import Hub

register = template.Library()

@register.simple_tag(takes_context=True)
def numberofstories(context, hub):
    request = context['request']
    rational = False
    if request.META['HTTP_HOST'] == "rationalfiction.io" or \
       request.META['HTTP_HOST'] == "localhost:8000":
        rational = True

    # fictionhub includes rational                
    # if rational:
    #     stories = hub.posts.filter(published = True, rational=rational)
    # else:
    #     stories = hub.posts.filter(published = True)

    stories = hub.posts.filter(published = True, rational=rational)
    number = stories.count()
    return number
 
