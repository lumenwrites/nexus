import datetime
from django.utils.timezone import utc

def rank_hot(stories, top=180, consider=1000):
    # top - number of stories to show,
    # consider - number of latest stories to rank
    
    def score(post, gravity=1.8, timebase=120):
        # number_of_comments = len(post.comments.all())
        rating = (post.score + 1)**0.8 # + number_of_comments
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        age = int((now - post.pub_date).total_seconds())/60
        return rating/(age+timebase)**1.8

    latest_stories = stories.order_by('-pub_date')#[:consider]
    #comprehension, stories with rating, sorted
    stories_with_rating = [(score(story), story) for story in latest_stories]
    #ranked_stories = sorted(stories_with_rating, reverse = True) - old but worked
    ranked_stories = sorted(latest_stories, key=score, reverse = True)
    #strip away the rating and return only stories
    # return [story for _, story in ranked_stories][:top] - old but worked
    return ranked_stories

def rank_top(stories, timespan = None):
    if timespan == "day":
        day = datetime.datetime.utcnow().replace(tzinfo=utc).__getattribute__('day')
        stories = stories.filter(pub_date__day = day)        
    elif timespan == "month":
        month = datetime.datetime.utcnow().replace(tzinfo=utc).__getattribute__('month')
        stories = stories.filter(pub_date__month = month)        
    elif timespan == "all-time":
        year = datetime.datetime.utcnow().replace(tzinfo=utc).__getattribute__('year')
        stories = stories.filter(pub_date__year = year)                
    
    top_stories = stories.order_by('-score')
    return top_stories



def age(timestamp):
    now = datetime.datetime.utcnow().replace(tzinfo=utc)
    created_at = datetime.datetime.fromtimestamp(timestamp).replace(tzinfo=utc)
    
    age_in_minutes = int((now-created_at).total_seconds())/60

    if age_in_minutes < 60:
        value = age_in_minutes
        precision = 'minute'
    elif age_in_minutes < 60*24:
        value = age_in_minutes//60
        precision = 'hour'
    else:
        value = age_in_minutes//(60*24)
        precision = 'day'

    age_string = "%d %s%s ago" % (value, precision, ('s' if value > 1 else ''))
    return age_string
