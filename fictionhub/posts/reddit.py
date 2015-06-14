import praw
import webbrowser


r = praw.Reddit('OAuth testing example by /u/raymestalez ver 0.1')

r.set_oauth_app_info(client_id="p19C3LIMRo-79w",
                     client_secret="pYv92Pp2FfbAS6AzQbxbQC5I75g",
                     redirect_uri='http://127.0.0.1:65010/'
                     'authorize_callback')

def get_access():
    url = r.get_authorize_url('uniqueKey', 'identity submit', True)

    webbrowser.open(url)


def get_user_info():    
    access_information = r.get_access_information('Wyi6kUY72ot_Sugt3F_CzcyZeCk')
    authenticated_user = r.get_me()
    print ("username: " + str(authenticated_user.name), "userkarma: " + str(authenticated_user.link_karma))


get_access()
# get_user_info()
