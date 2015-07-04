# to count words
from string import punctuation
import re
import datetime

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from .models import User
from .forms import RegistrationForm, UserForm

from posts.models import Post

# import praw
# import webbrowser

def subscribe(request, username):
    userprofile = User.objects.get(username=username)
    if not request.user.is_anonymous():
        user = request.user
        user.subscribed_to.add(userprofile)
        user.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 
    else:
        return HttpResponseRedirect('/login/')    

def unsubscribe(request, username):
    userprofile = User.objects.get(username=username)    
    user = request.user
    user.subscribed_to.remove(userprofile)
    user.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 

def about(request, username):
    userprofile = get_object_or_404(User, username=username)    
    subscribed_to = request.user.subscribed_to.all()
    return render(request, 'profiles/about.html',{
        'userprofile':userprofile,
        'subscribed_to':subscribed_to,
        'filterurl': "/user/"+request.user.username
    })

@login_required
def preferences(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')

    if request.method == 'POST':
        form = UserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            # user = request.user
            # user.set_password(form.cleaned_data.get('password'))
            # user.save()
            return HttpResponseRedirect('/preferences/')            
    else:
        form = UserForm(instance=request.user)
        # password_change_form = PasswordChangeForm(user=request.user)
    
    return render(request, "profiles/prefs.html", {
        'form': form,
        # 'password_change_form': password_change_form,
        'title': "Preferences"                
    })

@login_required
def update_password(request):
    form = PasswordChangeForm(user=request.user)

    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return HttpResponseRedirect('/preferences/')                        
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, "profiles/prefs.html", {
        'form': form,
        # 'message': "Error, try again.",
        'title': "Change Password"                        
    })


def login_or_signup(request):
    # If already logged in - get out of here
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')

    nextpage = request.GET.get('next', '/')
    authenticate_form = AuthenticationForm(None, request.POST or None)
    # register_form = UserCreationForm()
    register_form = RegistrationForm()
    register_form.fields['password1'].widget.attrs['placeholder'] = "Password"
    register_form.fields['password2'].widget.attrs['placeholder'] = "Repeat Password"        
    return render(request, "profiles/login.html", {
        'authenticate_form': authenticate_form,
        'register_form': register_form,
        'nextpage': nextpage,                
    })


# Only log in
def authenticate_user(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
 
    # Initialize the form either fresh or with the appropriate POST data as the instance
    auth_form = AuthenticationForm(None, request.POST or None)
 
    # Ye Olde next param so common in login.
    # I send them to their default profile view.
    nextpage = request.GET.get('next', '/')
 
    # The form itself handles authentication and checking to make sure passowrd and such are supplied.
    if auth_form.is_valid():
        login(request, auth_form.get_user())
        return HttpResponseRedirect(nextpage)
 
    return render(request, 'profiles/form-invalid.html', {
        'form': auth_form,
        'title': 'User Login',
        'next': nextpage,
    })

# Only sign up
def register(request):
    rational = False
    if request.META['HTTP_HOST'] == "rationalfiction.io" or \
       request.META['HTTP_HOST'] == "localhost:8000":
        rational = True

    if request.method == 'POST':
        # form = UserCreationForm(request.POST)
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # new_user = form.save()
            user = User.objects.create_user(form.cleaned_data['username'], None, form.cleaned_data['password1'])
            user.email = form.cleaned_data['email']
            user.rational = rational
            if rational:
                user.approved = True
            user.save()

            # log user in after signig up
            username = request.POST['username']
            password = request.POST['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            
            return HttpResponseRedirect("/")
    else:
        form = UserCreationForm()
    return render(request, "profiles/form-invalid.html", {
        'form': form,
    })


def grant_reddit_access(request):
    pass

def stats(request):
    user = request.user
    posts = Post.objects.filter(author=user)
    today = datetime.date.today()
    wordcount = 0
    this_month = 0
    r = re.compile(r'[{}]'.format(punctuation))

    days = [0]*(today.day+1)
    for post in posts:
        no_punctuation = r.sub(' ',post.body)
        number_of_words_in_a_post = len(no_punctuation.split())
        wordcount += number_of_words_in_a_post
        pub_date = post.pub_date
        if post.pub_date.month == today.month and post.pub_date.day < len(days):
            days[post.pub_date.day] += number_of_words_in_a_post
            this_month += number_of_words_in_a_post
    
    return render(request, "profiles/test.html", {
        'wordcount': wordcount,
        'this_month': this_month,        
        'pub_date':pub_date,
        'days':days
    })
