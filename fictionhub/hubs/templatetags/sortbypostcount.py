from django import template
from django.db.models import Count

from hubs.models import Hub

register = template.Library()

@register.filter
def sortbypostcount(children,request):
    # request = context['request']
    rational = False
    if request.META['HTTP_HOST'] == "rationalfiction.io" or \
       request.META['HTTP_HOST'] == "localhost:8000":
        rational = True

    children_postcount = []
    for child in children:
        child.postcount = child.posts.filter(published=True,rational=rational).count()
        children_postcount.append(child)

    children_postcount.sort(key=lambda x: x.postcount, reverse = True)
    # children = children.annotate(number_of_posts=Count('posts')).order_by('-number_of_posts')
    return children_postcount
 
