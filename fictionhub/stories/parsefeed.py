import feedparser
feed = feedparser.parse("http://orangemind.io/feeds/all.atom.xml")

for entry in entries:
    print(entry.title)
