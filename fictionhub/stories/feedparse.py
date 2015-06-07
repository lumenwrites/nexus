from .models import Story

# import feedparser
# feed = feedparser.parse("http://orangemind.io/feeds/all.atom.xml")

# for entry in feed.entries:
#     print(entry.title)

print(Story.objects.all())
