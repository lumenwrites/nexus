import praw
import webbrowser
import os


r = praw.Reddit('OAuth testing example by /u/raymestalez ver 0.1')

r.set_oauth_app_info(client_id=os.environ['CLIENT_ID'],
                     client_secret=os.environ['CLIENT_SECRET'],
                     redirect_uri='http://127.0.0.1:65010/'
                     'authorize_callback')

def get_access():
    url = r.get_authorize_url('uniqueKey', 'identity submit', True)

    webbrowser.open(url)



def get_user_info():    
    access_information = r.get_access_information('qoZBzSvvvfcKeHwK3BemX91kUlA')
    authenticated_user = r.get_me()
    print ("username: " + str(authenticated_user.name), "userkarma: " + str(authenticated_user.link_karma))



def submit_post():
    subreddit = r.get_subreddit('OrangeMind')
    thread = list(r.search("test", subreddit=subreddit, sort="new", syntax='cloudsearch'))[0]
    # print(thread.__dict__.keys())
    # print(thread.selftext)
    access_information = r.get_access_information('ZyiSO3y0VH7Jm9pZol97e0f5v-g')
    r.refresh_access_information(access_information['refresh_token'])
    r.set_access_credentials(**access_information)
    authenticated_user = r.get_me()
    print ("username: " + str(authenticated_user.name), "userkarma: " + str(authenticated_user.link_karma))    
    # r.refresh_access_information(access_information['qoZBzSvvvfcKeHwK3BemX91kUlA'])
    # thread.add_comment("test comment!")

# get_access()
# get_user_info()
submit_post()
