# standard library imports
import re, praw
from xml.etree.ElementTree import Element, SubElement, tostring # for rss
import json # for temporary post api. Replace with REST.
import feedparser

# core django components
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import * # for rss
# for 404
from django.shortcuts import render_to_response
from django.template import RequestContext
# date
from datetime import datetime
from django.utils.timezone import utc
from time import mktime
# slugify dropbox title
from django.template.defaultfilters import slugify

# My own stuff
# utility functions
from comments.utils import get_comment_list
from .utils import rank_hot, rank_top
# Forms
from .forms import PostForm
from comments.forms import CommentForm
from hubs.forms import HubForm
# Models
from .models import Post
from profiles.models import User
from hubs.models import Hub
from comments.models import Comment

#dropbox
import os
import dropbox
from markdown import Markdown



def posts(request, rankby="hot", timespan="all-time",
            filterby="", hubslug="", username="", challenge=""):
    # for user profile navbar
    userprofile = []
    filterurl = ""
    if not challenge:
        challenge = []

    if not request.user.is_anonymous():
        subscribed_to = request.user.subscribed_to.all()
    else:
        subscribed_to = []
    
    if filterby == "subscriptions":
        subscribed_to = request.user.subscribed_to.all()
        posts = Post.objects.filter(author=subscribed_to, published=True)
        filterurl="/subscriptions" # to add to href  in subnav
    elif filterby == "hub":
        hub = Hub.objects.get(slug=hubslug)
        # Show posts from all the children hubs? Don't know how to sort.
        # children = Hub.objects.filter(parent=hub)
        # hubs = []
        posts = Post.objects.filter(hubs=hub, published=True)
        filterurl="/hub/"+hubslug # to add to href  in subnav
    elif filterby == "user":
        userprofile = get_object_or_404(User, username=username)
        if request.user == userprofile:
            # If it's my profile - display all the posts, even unpublished.
            posts = Post.objects.filter(author=userprofile)
        else:
            posts = Post.objects.filter(author=userprofile, published=True)
        filterurl="/user/"+username # to add to href  in subnav
    elif filterby == "challenges":
        posts = Post.objects.filter(post_type = "challenge", published=True)
        rankby = "new"
    elif filterby == "challenge":
        challenge = Post.objects.get(slug=challenge)
        if challenge.state == "voting":
            rankby = "new" # later do random
        elif challenge.state == "completed":            
            rankby = "top"
        posts = Post.objects.filter(parent=challenge, published=True)
    else:
        posts = Post.objects.filter(published=True)
        filterurl="/stories"

    if rankby == "hot":
        post_list = rank_hot(posts, top=32)
    elif rankby == "top":
        post_list = rank_top(posts, timespan = timespan)
    elif rankby == "new":
        post_list = posts.order_by('-pub_date')
    else:
        post_list = []


    # Pagination
    paginator = Paginator(post_list, 25)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)    

    # Disable upvoted/downvoted
    if request.user.is_authenticated():
        upvoted = request.user.upvoted.all()
        downvoted = request.user.downvoted.all()                
    else:
        upvoted = []
        downvoted = []        

    
    # if not posts:
    #     return HttpResponseRedirect('/404')

    hubs = Hub.objects.all().order_by('id')

    return render(request, 'posts/posts.html',{
        'posts':posts,
        'upvoted': upvoted,
        'downvoted': downvoted,
        'filterby':filterby,
        'filterurl': filterurl,                
        'rankby': rankby,
        'timespan': timespan,
        'userprofile':userprofile,
        'subscribed_to': subscribed_to,
        'hubs': hubs,
        'challenge':challenge
    })

# Voting
def upvote(request):
    post = get_object_or_404(Post, id=request.POST.get('post-id'))
    post.score += 1
    post.save()
    post.author.karma += 1
    post.author.save()
    user = request.user
    user.upvoted.add(post)
    user.save()
    return HttpResponse()

def downvote(request):
    post = get_object_or_404(Post, id=request.POST.get('post-id'))
    if post.score > 0:
        post.score -= 1
        post.author.karma -= 1        
    post.save()
    post.author.save()
    user = request.user
    user.downvoted.add(post)
    user.save()
    return HttpResponse()

def unupvote(request):
    post = get_object_or_404(Post, id=request.POST.get('post-id'))
    post.score -= 1
    post.save()
    post.author.karma = 1
    post.author.save()
    user = request.user
    user.upvoted.remove(post)
    user.save()
    return HttpResponse()

def undownvote(request):
    post = get_object_or_404(Post, id=request.POST.get('post-id'))
    post.score += 1
    post.author.karma += 1        
    post.save()
    post.author.save()
    user = request.user
    user.downvoted.remove(post)
    user.save()
    return HttpResponse()
            
def post(request, story, comment_id="", chapter="", rankby="new", filterby=""):
    try:
        story = Post.objects.get(slug=story)
    except:
        return HttpResponseRedirect('/404')
        

    try:
        # doesn't work if 2 chapters #1
        first_chapter = Post.objects.get(parent=story, number=1)
        # first_chapter = story.children.filter(number=1)[0]
    except:
        first_chapter = []
    

    # If chapter
    if chapter:
        chapter = Post.objects.get(slug=chapter)
        first_chapter = []  # empty first chapter to show the right button in post template
        try:
            prev_chapter = Post.objects.get(parent=story, number=chapter.number-1)
        except:
            prev_chapter = []

        try:
            next_chapter = Post.objects.get(parent=story, number=chapter.number+1)
        except:
            next_chapter = []
    else:
        chapter = []
        prev_chapter = []
        next_chapter = []
        
    
    hubs = story.hubs.all()
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False) # return post but don't save it to db just yet
            comment.author = request.user
            comment.parent = None
            if chapter:
                comment.post = chapter                
            else:
                comment.post = story
            comment.save()
            if comment.comment_type == "comment":
                if chapter:
                    return HttpResponseRedirect('/story/'+story.slug+'/'+chapter.slug+'#comments')
                else:
                    return HttpResponseRedirect('/story/'+story.slug+'#comments')
            else:
                if chapter:
                    return HttpResponseRedirect('/story/'+story.slug+'/'+chapter.slug+'/reviews#comments')
                else:
                    return HttpResponseRedirect('/story/'+story.slug+'/reviews#comments')
                
    else:
        form = CommentForm()

    if request.user.is_authenticated():
        upvoted = request.user.upvoted.all()
        downvoted = request.user.downvoted.all()                
    else:
        upvoted = []
        downvoted = []  

    # For subscribe button
    if not request.user.is_anonymous():
        subscribed_to = request.user.subscribed_to.all()
    else:
        subscribed_to = []


    # Get top lvl comments
    if filterby == "reviews":
        filterurl = "reviews"
        if chapter:
            top_lvl_comments = Comment.objects.filter(post = chapter,
                                                      comment_type="review",
                                                      parent = None)
        else:
            top_lvl_comments = Comment.objects.filter(post = story,
                                                      comment_type="review",
                                                      parent = None)
    else:
        if chapter:
            top_lvl_comments = Comment.objects.filter(post = chapter,
                                                      comment_type="comment",
                                                      parent = None)
        else:
            top_lvl_comments = Comment.objects.filter(post = story,
                                                      comment_type="comment",
                                                      parent = None)

    # Rank comments
    if rankby == "hot":
        ranked_comments = rank_hot(top_lvl_comments, top=32)
    elif rankby == "top":
        ranked_comments = rank_top(top_lvl_comments, timespan = "all-time")
    elif rankby == "new":
        ranked_comments = top_lvl_comments.order_by('-pub_date')
    else:
        ranked_comments = []

    # Permalink to one comment
    if comment_id:
        comment = []
        comment.append(Comment.objects.get(id = comment_id))
        ranked_comments = comment


    # Nested comments
    comments = list(get_comment_list(ranked_comments, rankby=rankby))

    if request.user.is_authenticated():
        comments_upvoted = request.user.comments_upvoted.all()
        comments_downvoted = request.user.comments_downvoted.all()                
    else:
        comments_upvoted = []
        comments_downvoted = []  

    if chapter:
        post = chapter
    else:
        post = story

    if filterby:
        filterby = "/" + filterby
    else:
        filterby = "/comments"
    return render(request, 'posts/post.html',{
        'post': post,
        'first_chapter':first_chapter,
        'chapter': chapter,
        'prev_chapter': prev_chapter,
        'next_chapter': next_chapter,       
        'upvoted': upvoted,
        'downvoted': downvoted,
        'comments': comments,
        'comments_upvoted': comments_upvoted,
        'comments_downvoted': comments_downvoted,
        'rankby': rankby,        
        'form': form,
        'hubs':hubs,
        'subscribed_to':subscribed_to,
        'filterby':filterby
    })

def post_create(request, story="", challenge=""):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False) # return post but don't save it to db just yet
            post.author = request.user
            # self upvote
            post.score += 1
            post.post_type = "story"
            if story:
                post.parent = Post.objects.get(slug=story)
                post.post_type = "chapter"
            if challenge:
                post.parent = Post.objects.get(slug=challenge)
            post.save()
            request.user.upvoted.add(post)            
            post.hubs.add(*form.cleaned_data['hubs'])
            hubs = post.hubs.all()
            for hub in hubs:
                if hub.parent:
                    post.hubs.add(hub.parent)
            # Hacky way to 
            # for hub in form.cleaned_data['hubs']:
            #     if hub.parent:
            #         post.hubs.add(hub.parent)
            #         if hub.parent.parent:
            #             post.hubs.add(hub.parent.parent)
            if story:
                return HttpResponseRedirect('/story/'+post.parent.slug+'/'+post.slug+'/edit')
            else:
                return HttpResponseRedirect('/story/'+post.slug+'/edit')
    else:
        form = PostForm()
        form.fields["hubs"].queryset = Hub.objects.filter(children=None).order_by('id')
        if challenge:
            challenge = Post.objects.get(slug=challenge)
        else:
            challenge =[]

    if story:
        story = Post.objects.get(slug=story)
        return render(request, 'posts/edit.html', {
            'story':story,        
            'form':form,
            'action':'chapter_create',
            'challenge':challenge
            
        })
    else:
        return render(request, 'posts/create.html', {
            'form':form,
            'hubs':Hub.objects.all(),
            'challenge':challenge            
        })


def post_edit(request, story, chapter=""):
    story = Post.objects.get(slug=story)
    action = "story_edit"
    if chapter:
        chapter = Post.objects.get(slug=chapter)
        action="chapter_edit"


    # throw him out if he's not an author
    if request.user != story.author:
        return HttpResponseRedirect('/')        

    if request.method == 'POST':
        if chapter:
            form = PostForm(request.POST,instance=chapter)            
        else:
            form = PostForm(request.POST,instance=story)
        if form.is_valid():
            post = form.save(commit=False) # return post but don't save it to db just yet
            if chapter:
                post.post_type = "chapter"
                post.parent = story
            post.save()
            post.hubs = []
            post.hubs.add(*form.cleaned_data['hubs'])
            hubs = post.hubs.all()
            for hub in hubs:
                if hub.parent:
                    post.hubs.add(hub.parent)
            if chapter:
                return HttpResponseRedirect('/story/'+story.slug+'/'+post.slug+'/edit')
            else:
                return HttpResponseRedirect('/story/'+post.slug+'/edit')
    else:
        if chapter:
            form = PostForm(instance=chapter)            
        else:
            form = PostForm(instance=story)
        form.fields["hubs"].queryset = Hub.objects.filter(children=None).order_by('id')        

    return render(request, 'posts/edit.html', {
        'story':story,
        'chapter':chapter,            
        'form':form,
        'action':action
    })

def chapter_up(request, story, chapter):
    story = Post.objects.get(slug=story)
    chapter = Post.objects.get(slug=chapter) # add post=post, to not confuse with others!

    # throw him out if he's not an author
    if request.user != story.author:
        return HttpResponseRedirect('/')        

    try:
        following_chapter = story.chapters.get(number=chapter.number+1)
        following_chapter.number -= 1
        following_chapter.save()
    except:
        pass

    chapter.number += 1
    chapter.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))            

def chapter_down(request, story, chapter):
    story = Post.objects.get(slug=story)
    chapter = Post.objects.get(slug=chapter) # add post=post, to not confuse with others!

    # throw him out if he's not an author
    if request.user != story.author:
        return HttpResponseRedirect('/')        

    if chapter.number > 0:    
        try:
            following_chapter = story.chapters.get(number=chapter.number-1)
            following_chapter.number += 1
            following_chapter.save()
        except:
            pass

        chapter.number -= 1
        chapter.save()
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def post_delete(request, story, chapter=""):
    story = Post.objects.get(slug=story)
    if chapter:
        post = Post.objects.get(slug=chapter)
    else:
        post = story

    # throw him out if he's not an author
    if request.user != post.author:
        return HttpResponseRedirect('/')        

    post.delete()
    if chapter:
        return HttpResponseRedirect('/story/'+story.slug + '/edit') # to post list
    else:
        return HttpResponseRedirect('/') # to post list


def post_publish(request, story):
    post = Post.objects.get(slug=story)

    # throw him out if he's not an author
    if request.user != post.author:
        return HttpResponseRedirect('/')        

    post.published = True
    post.save()
    return HttpResponseRedirect('/story/'+post.slug+'/edit')


def post_unpublish(request, story):
    post = Post.objects.get(slug=story)

    # throw him out if he's not an author
    if request.user != post.author:
        return HttpResponseRedirect('/')        

    post.published = False
    post.save()
    return HttpResponseRedirect('/story/'+post.slug+'/edit')




def page_404(request):
    response = render_to_response('404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response


def post_feed(request, post):
    post = Post.objects.get(slug=post)
    rss = Element('rss')
    rss.set("version","2.0")

    channel = SubElement(rss,'channel')

    title = SubElement(channel,'title')
    title.text = post.title

    link = SubElement(channel,'link')
    link.text = "http://fictionhub.io/story/"+post.slug # request.build_absolute_uri(reverse("post"))

    desc = SubElement(channel,'description')
    desc.text = post.description

    chapters = post.chapters.all()

    for index in chapters:
        item = SubElement(channel,'item')

        title_c = SubElement(item,'title')
        title_c.text = index.title
        
        link = SubElement(item,'link')
        #link.text = request.build_absolute_uri(index.get_absolute_url())
        link.text = "http://fictionhub.io/story/"+post.slug
    return HttpResponse(tostring(rss, encoding='UTF-8'), content_type='application/xml')


# Post API. Replace with REST.
def post_json(request, slug):
    try:
        post = Post.objects.get(slug=slug)
    except:
        return HttpResponseRedirect('/404')

    res = {}
    res['title'] = post.title
    res['author'] = post.author.username
    res['chapters'] = []
    chapters = post.chapters.all()

    for index in chapters:
        res['chapters'].append({"title": index.title, "number": index.number, "text": index.body})

    return HttpResponse(json.dumps(res), content_type='application/json')


# import feed
def feed_import(request, username):
    feed = feedparser.parse("http://orangemind.io/feeds/all.atom.xml")

    author = request.user
    
    for entry in feed.entries:
        import_entry = False
        # Check if post has "fictionhub" in it's tags
        if "tags" in entry.keys():
            for tag in entry.tags:
                if tag.term == "fictionhub":
                    import_entry = True
        if import_entry:
            title = entry.title
            slug = entry.link.rsplit('/',1)[-1]
            body = entry.description
            date = datetime.fromtimestamp(mktime(entry.updated_parsed))        
            try:
                # Open existing post
                post = Post.objects.get(slug=slug)
            except:
                # Import post
                post = Post(slug=slug)
                post.score = 1
                
            post.title = title
            post.body = body
            post.date = date
            post.author = author
            for tag in entry.tags:
                # post.title = post.title + " " + tag.term
                try:
                    hub = Hub.objects.get(slug=tag.term)
                    post.hubs.add(hub)
                except:
                    pass
            post.post_type = "story"
            post.imported = True
            post.published = True
            post.save(slug=slug)
    return HttpResponse()


def dropbox_import(request):
    author = request.user
    
    
    access_token = os.environ["ACCESS_TOKEN"]
    client = dropbox.client.DropboxClient(access_token)
    folder_metadata = client.metadata('/')

    teststring = ""
    imported = ""
    updated = ""
    for file in folder_metadata["contents"]:
        if not file["is_dir"]:
            path = file["path"]
            f, metadata = client.get_file_and_metadata(path)
            text = f.read()
            text = text.decode("utf-8")
    
            md = Markdown(extensions = ['meta', 'codehilite'])
            content = md.convert(text)
            metadata = {}
            for name, value in md.Meta.items():
                metadata[name] = value[0]
                teststring += name + ": " + value[0] + "<br/>"
    
            # teststring += "Title: " + metadata['title'] + "\n" + \
            #               "Date: " + metadata['date'] + \
            #               "Content: " + content
    
            try:
                tags = metadata["tags"].split(",")
            except:
                tags = []
            import_entry = False
            # Check if post has "fictionhub" in it's tags
            for tag in tags:
                if tag == "fictionhub":
                    import_entry = True
    
            if import_entry:
                title = metadata["title"]
                try:
                    slug = metadata["slug"]
                except:
                    slug = slugify(title)
                body = content
                date = datetime.strptime(metadata['date'], "%Y-%m-%d")# %H:%M:%S.%f
                try:
                # Open existing post
                    post = Post.objects.get(slug=slug)
                    updated += title + " " 
                except:
                    # Import post
                    post = Post(slug=slug)
                    post.score = 1
                    imported += title + " "
    
                    # If it is a writing prompt
                    # try and see if it has metadata["promptslug"]
                    # check if propmt with this slug exists
                    # if it does - set it as parent
                    # if it doesn't - create it and set it as parent.
                    # don't forget to set it's type as "prompt"
    
                post.title = title
                post.body = body
                post.date = date
                post.author = author
                for tag in tags:
                    # post.title = post.title + " " + tag.term
                    try:
                        hub = Hub.objects.get(slug=tag)
                        post.hubs.add(hub)
                    except:
                        pass
                post.post_type = "story"
                post.imported = True
                post.published = True
                try:
                    if metadata['published'] == "False":
                        post.published = False
                except:
                    pass
                post.save(slug=slug)

                if imported:
                    teststring += "Imported: " + imported + "<br/>"
                if updated:
                    teststring += "Updated: " + updated + "<br/>"
                
    return render(request, 'posts/test.html', {
        'teststring': teststring,
    })
           

def age(timestamp):
    now = datetime.utcnow().replace(tzinfo=utc)
    created_at = datetime.fromtimestamp(timestamp).replace(tzinfo=utc)
    
    age_in_minutes = int((now-created_at).total_seconds())/60

    return age_in_minutes



def prompts(request):
    import praw
    r = praw.Reddit(user_agent='Request new prompts from /r/writingprompts by /u/raymestalez')
    subreddit = r.get_subreddit('writingprompts')
    prompts = subreddit.get_new(limit=64)
    new_prompts = list(prompts)
    prompts = []

    # less than 5 replies, more than 1 upvote and less than 60 minutes old
    for prompt in new_prompts:
        if (prompt.score > 1) \
        and ((prompt.num_comments-2) < 5) \
        and (age(prompt.created_utc) < 60):
            if prompt.num_comments > 0:
                prompt.num_comments -= 2 # remove 2 fake replies
            prompts.append(prompt)

    # sort by score
    prompts.sort(key=lambda p: p.score, reverse=True)
            
        
    return render(request, 'posts/prompt.html', {
        'prompts': prompts[:8],
    })



def prompt(request):
    import praw
    r = praw.Reddit(user_agent='Request new prompts from /r/writingprompts by /u/raymestalez')
    subreddit = r.get_subreddit('writingprompts')
    prompts = subreddit.get_new(limit=64)
    new_prompts = list(prompts)
    prompts = []

    # less than 5 replies, more than 1 upvote and less than 60 minutes old
    for prompt in new_prompts:
        if (prompt.score > 1) \
        and ((prompt.num_comments-2) < 5) \
        and (age(prompt.created_utc) < 60):
            if prompt.num_comments > 0:
                prompt.num_comments -= 2 # remove 2 fake replies
            prompts.append(prompt)

    # sort by score
    prompts.sort(key=lambda p: p.score, reverse=True)

    prompt = prompts[0]

    # save prompt
    # author = request.user
    # title = prompt.title
    # body = ""
    # slug = slugify(title[:32]) # learn to remove [WP] from slug

    # try:
    #     post = Post.objects.get(slug=slug)
    # except:
    #     post = Post(slug=slug)
    #     post.score = 1

    
    # post.title = title
    # post.body = body
    # post.author = author # separate account?
    # post.post_type = "prompt"
    # post.published = True # False
    # post.imported = True    
    # post.save(slug=slug)    
    
    return HttpResponse(prompt.title)
    


def prompt_import(request):
    import praw
    r = praw.Reddit(user_agent='Request new prompts from /r/writingprompts by /u/raymestalez')
    subreddit = r.get_subreddit('writingprompts')
    prompts = subreddit.get_new(limit=64)
    new_prompts = list(prompts)
    prompts = []

    # less than 5 replies, more than 1 upvote and less than 60 minutes old
    for prompt in new_prompts:
        if (prompt.score > 1) \
        and ((prompt.num_comments-2) < 5) \
        and (age(prompt.created_utc) < 60):
            if prompt.num_comments > 0:
                prompt.num_comments -= 2 # remove 2 fake replies
            prompts.append(prompt)

    # sort by score
    prompts.sort(key=lambda p: p.score, reverse=True)

    prompt = prompts[0]

    # save prompt
    author = request.user
    title = prompt.title
    body = ""
    slug = slugify(title[:32]) # learn to remove [WP] from slug

    # try:
    #     post = Post.objects.get(slug=slug)
    # except:
    #     post = Post(slug=slug)
    #     post.score = 1

    
    # post.title = title
    # post.body = body
    # post.author = author # separate account?
    # post.post_type = "prompt"
    # post.published = True # False
    # post.imported = True    
    # post.save(slug=slug)    
    
    return HttpResponse("<span id='title'>"+title+"</span>" + \
                        "<span id='slug'>"+slug+"</span>")
    


# TODO: replace with CBVs
# from django.views.generic import View,TemplateView, ListView, DetailView, FormView, CreateView
# from django.shortcuts import render

# from .models import Post
# from .forms import PostForm
# from .utils import rank_hot, rank_top



# class PostsView(ListView):
#     model = Post
#     template_name = "posts/posts.html"

#     def get_queryset(self):
#         posts = Post.objects.all()

#         rankby = self.kwargs['rankby']
#         if rankby == "hot":
#             post_list = rank_hot(posts, top=32)
#         elif rankby == "top":
#             post_list = rank_top(posts, timespan = timespan)
#         elif rankby == "new":
#             post_list = posts.order_by('-pub_date')
#         else:
#             post_list = []

#         return posts

#     def get_context_data(self, **kwargs):
#         context = super(PostsView, self).get_context_data(**kwargs)
#         context['rankby'] =  self.kwargs['rankby']
#         return context    
        

# class PostView(DetailView):
#     model = Post
#     template_name = "posts/post.html"    

# class PostCreate(CreateView):
#     model = Post
#     form_class = PostForm
#     template_name = "posts/create.html"    

# class PostEdit(FormView):
#     template_name = "posts/edit.html"    
#     form_class = PostForm

#     success_url = '/thanks/'

#     def form_valid(self, form):
#         # This method is called when valid form data has been POSTed.
#         # It should return an HttpResponse.
#         form.send_email()
#         return super(ContactView, self).form_valid(form)    

# TODO: dry it in one function
# def vote(request):
#     post = Post.objects.get(id=request.POST.get('post-id'))
#     vote =  request.POST.get('vote')
#     user = request.user

#     if post in user.upvoted:    # unupvote
#         post.score -= 1
#         post.author.karma -= 1
#         user.upvoted.remove(post)
#     elif post in user.downvoted:# undownvote
#         post.score += 1
#         post.author.karma += 1
#         user.downvoted.remove(post)
#     elif vote == "up":          # upvote
#         post.score += 1
#         post.author.karma += 1
#         user.upvoted.add(post)
#     elif vote == "down":        # downvote
#         if post.score > 0:
#             post.score -= 1
#             post.author.karma -= 1
#             user.downvoted.add(post)

#     post.save()
#     post.author.save()
#     user.save()

#     return HttpResponse()
