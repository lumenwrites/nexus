from django.core.mail import send_mail # for email
from django.core.mail import EmailMultiAlternatives
from notifications.models import Message


def send_comment_email(from_username,to_email,story_url,comment_body):
    if comment.post.author.email_comments:

        try:
            email = to_email
            send_mail(topic, body, 'raymestalez@gmail.com', [email], fail_silently=False)
        except:
            pass



        

def send_notification_email(message):
    from_username = message.from_user.username
    to_user = message.to_user
    send_email = False
    if to_user.rational:
        base_url = "http://rationalfiction.io"
    else:
        base_url = "http://fictionhub.io"
    if to_user.rational:
        website_name = "rationalfiction"
    else:
        website_name = "fictionhub"


    if message.message_type == "upvote" and to_user.email_upvotes:
        send_email = True
        story_url = message.story.get_absolute_url()
        story_title = message.story.title
        
        topic = website_name + ": " + from_username + " upvoted your story "  + story_title
        body = from_username + " upvoted your story\n" +\
               base_url+story_url
        body += "\n\nYou can manage your email notifications in preferences:\n" +\
                base_url + "/preferences/"
    elif message.message_type == "subscriber"  and to_user.email_subscribers:
        send_email = True

        topic = website_name + ": " + from_username + " subscribed to your stories!"
        body = from_username + " subscribed to your stories!"
        body += "\n\nYou can manage your email notifications in preferences:\n" +\
                base_url+"/preferences/"
    elif message.message_type == "comment" and to_user.email_comments:
        send_email = True
        story_url = message.story.get_absolute_url()
        comment_body = message.comment.body

        topic = website_name+": " + from_username + " has commented on your story "
        body = from_username + " has left a comment on your story\n" +\
               base_url+story_url+ "\n" +\
               "'" + comment_body[:64] + "...'"
        body += "\n\nYou can manage your email notifications in preferences:\n" +\
                base_url+"/preferences/"
    elif message.message_type == "newstory" and to_user.email_subscriptions:
        send_email = True
        story_url = message.story.get_absolute_url()
        story_title = message.story.title

        topic = website_name+": " + from_username + " has published a story " + story_title
        body = from_username + " has published a new story\n" +\
               '"'+story_title+'"\n'+\
               base_url+story_url+ "\n"
        body += "\n\nYou can manage your email notifications in preferences:\n" +\
                base_url+"/preferences/"        
    elif message.message_type == "message" and to_user.email_comments:
        send_email = True

        topic = website_name+ ": " + from_username + " has sent you a message "
        body = from_username + " has  sent you a message:\n" +\
               "'" + message.subject.title + "'\n" + \
               message.body + "\n" + \
               base_url+"/subject/" + str(message.subject.pk) + "/"
        body += "\n\nYou can manage your email notifications in preferences:\n" +\
                base_url+"/preferences/"

    body += "\n\n P.S. \n "+website_name+", including email notifications, is still in beta.\n If you have any comments, questions or suggestions - feel free to reply to this message, I welcome any feedback =)"
        

    if send_email == True:
        try:
            email = to_user.email # "raymestalez@gmail.com" 
            send_mail(topic, body, 'raymestalez@gmail.com', [email], fail_silently=False)
        except:
            pass

    message.email_sent = True
    message.save()

            
def send_email_notifications():
    messages = Message.objects.filter(email_sent=False, isread=False)
    teststring = ""
    for message in messages:
        send_notification_email(message)
        teststring += str(message) + "</br>"

    return teststring
