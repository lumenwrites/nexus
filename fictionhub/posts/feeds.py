from markdown import Markdown

from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from django.shortcuts import get_object_or_404

from .models import Post
from profiles.models import User



class MainFeed(Feed):
    title = "fictionhub"
    link = "/feed/"
    description = "fictionhub"

    def items(self):
        return Post.objects.filter(published=True,post_type="story").order_by('-pub_date')[:25]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        md = Markdown()
        return md.convert(item.body)

    # item_link is only needed if NewsItem has no get_absolute_url method.
    def item_link(self, item):
        return item.get_absolute_url()
    
def post_feed(request, story):
    story = Post.objects.get(slug=story)
    rss = Element('rss')
    rss.set("version","2.0")

    channel = SubElement(rss,'channel')

    title = SubElement(channel,'title')
    title.text = story.title

    link = SubElement(channel,'link')
    link.text = "/story/"+story.slug # request.build_absolute_uri(reverse("post"))

    desc = SubElement(channel,'description')
    desc.text = story.body

    chapters = story.children.all()

    for index in chapters:
        item = SubElement(channel,'item')

        title_c = SubElement(item,'title')
        title_c.text = index.title
        
        link = SubElement(item,'link')
        #link.text = request.build_absolute_uri(index.get_absolute_url())
        link.text = "/story/"+story.slug
    return HttpResponse(tostring(rss, encoding='UTF-8'), content_type='application/xml')





# rss
# rss
class UserFeed(Feed):
    title = "fictionhub latests stories"
    link = "/"
    feed_type = Atom1Feed

    def get_object(self, request, username):
        return get_object_or_404(User, username=username)

    def title(self, obj):
        return "fictionhub: %s latest stories" % obj.username

    def link(self, obj):
        return "http://fictionhub.io/user/" + obj.username
        # return "http://fictionhub.io/" +  str(item.get_absolute_url())
    
    def items(self, obj):
        return Post.objects.filter(published=True, author=obj).order_by("-pub_date")

    def item_title(self, item):
        return item.title
    
    def item_pubdate(self, item):
        return item.pub_date

    def item_description(self, item):
        md = Markdown()
        return md.convert(item.body)



