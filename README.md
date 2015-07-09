# Fictionhub

[![Join the chat at https://gitter.im/raymestalez/fictionhub](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/raymestalez/fictionhub?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

http://fictionhub.io/

My goal is to create the perfect place for people to share stories they write, discuss fiction/fanfiction, and help each other to get better at writing.

Project is in active development. This is a very early version, not even alpha yet, just a prototype.

![fictionhub](https://raw.githubusercontent.com/raymestalez/fictionhub/master/fictionhub/static/img/fictionhub.png)

<!-- # To Contributors -->
<!-- If you want to contribute to this project and make it more awesome, here's what you can do: -->

<!-- - First and foremost - feedback, ideas, and bug reports. -->
<!--   At this point I'm actively refactoring code, so it will be hard to make a meaningful contribution on the backend, but you can use the website and write me your thoughts about it or suggest new features to raymestalez@gmail.com - I will be very grateful =) -->
<!-- - If you are a javascript person - consider forking [this editor](https://github.com/lepture/editor) and figuring out how to make it work well on mobile. -->


# To-Do

[Major cleanup](https://gist.github.com/raymestalez/4710ae5b406bf1216199).  
The most basic features are done, now - refactoring and cleaning the code according to PEP8 and 2 Scoops of Django.


# Upcoming Features

- [Minor improvements](https://gist.github.com/raymestalez/890f98d47401431defbc)
- PMs
- Notifications(when someone comments, messages, etc)
  - Email updates on stories.
  - "News" page?  
	With comment replies, PMs, etc.
  - Notification icon
- RSS
  - Proper rss/atom feed for a story.
  - RSS of all stories.
- Import
  - Import RSS feeds
    - Full text import from wordpress feeds?
    - convert html to markdown
  - Import from fanfiction.net
    - Regularly update some stories.
  - Dropbox import:
      - Convenient way to authorize dropbox from preferences.
      - Look into directories, search within, directory name = hub
      - Changing titles
      - Deleting deleted files.  
        when slug doesn't exit?
  - Convenient manual import?
    - Paste preformatted text?
- REST API

&nbsp;

- Stats and metrics
  - Top users. Most active, by words/week, by karma, by views, etc.
- ePub/PDF export.
  html and markdown too?
- Wiki
  Edit history.
- Writing Prompts
  - with reddit reposting?
- Challenges
  - with reddit reposting? to /r/rational weekly challenges.

[Content](https://gist.github.com/raymestalez/4f27da8e0e03e52e1885)

## Future

- Search
  - Superior search engine.
	(now just using query to find matching text)
  - Filtering by hubs - union/intersection/exclude options.
	(search for stories containing all the hubs or any one of the hubs)
	with circle icons.
  - By author/date/length/rating/etc.
  - When there's too much hubs - search/filter hubs in the sidebar.
- Superior editor - especially on mobile.
- Recommendation engine.
    - top-rated stories by all users that gave 5 stars to a particular story?

<!--
- Store
  Brainstorm and discuss with community,
  decide on the best model, profitable to authors, convenient to readers:
	- Monthly subscription to all paid stories like on apple music?  
	  readers get access to everything for ~$10/mo,  
	  authors get rewarded in proportion to how much their stories have been read?
	- "Paid channels", subscribe to all author's updates? - meh
	- Micropayments? - meh
	- Ebook store?
    - Patreon kind of model? - meh
    - What else?
-->

&nbsp;

- [Maybe](https://gist.github.com/raymestalez/8252dfa470857c3c6764)
