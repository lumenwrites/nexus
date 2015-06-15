# coding: utf-8

import praw
import webbrowser
import os
r = praw.Reddit('OAuth testing example by /u/raymestalez ver 0.1')
r.set_oauth_app_info(client_id=os.environ['CLIENT_ID'],
                     client_secret=os.environ['CLIENT_SECRET'],
                     redirect_uri='http://127.0.0.1:65010/'
                     'authorize_callback')
r.set_oauth_app_info(client_id="USbv_fKdhw4zWg",
                     client_secret="IgXfdZXFUODkL7H39ZCrYSi-2_Y",
                     redirect_uri='http://127.0.0.1:65010/'
                     'authorize_callback')
url = r.get_authorize_url('uniqueKey', 'identity submit', True)
webbrowser.open(url)
access_information = r.get_access_information('2ToGAE-F-4Nu7r3ztASmQs4RcJM')
accesss_information
access_information
authenticated_user = r.get_me()
authenticated_user
subreddit = r.get_subreddit('OrangeMind')
thread = list(r.search("test", subreddit=subreddit, sort="new", syntax='cloudsearch'))[0]
thread
thread.selftext
thread.add_comment("test comment!")
thread.add_comment("another comment!")
authenticated_user = r.get_me()
r.get_me()
r.refresh_access_information(access_information['refresh_token'])
r.refresh_access_information(access_information['refresh_token'])
get_ipython().magic('save reddit')
