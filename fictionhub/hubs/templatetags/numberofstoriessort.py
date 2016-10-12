from django import template
from django.db.models import Count

from hubs.models import Hub

register = template.Library()

@register.filter
def numberofstoriessort(children):
    children_postcount = []
    for child in children:
        child.postcount = child.posts.filter(published=True,rational=True).count()
        children_postcount.append(child)
    children_postcount.sort(key=lambda x: x.postcount)
    
    return children
 
