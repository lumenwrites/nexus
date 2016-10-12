from django.shortcuts import render
from django.http import HttpResponseRedirect

from .models import Message, Subject
from profiles.models import User
from .utils import send_email_notifications

def notifications(request, notificationtype="all"):
    if notificationtype == "unread":
        messages = Message.objects.filter(to_user=request.user,
                                          isread=False).order_by('-pub_date')
        for message in messages:
            message.isread = True
            message.save()
        user = request.user
        user.new_notifications = False
        user.save()
    else:
        messages = Message.objects.filter(to_user=request.user).order_by('-pub_date')
    
    return render(request, 'notifications/notifications.html', {
        'messages':messages,
        'notificationtype':notificationtype,
    })


def send_message(request, username=""):
    if request.method == 'POST':
        to_user = User.objects.get(username=username)
        title = request.POST.get('title')
        subject = Subject(title = title)
        subject.save()
        body = request.POST.get('body')
        message = Message(from_user=request.user,
                          to_user=to_user,
                          subject = subject,
                          body=body,
                          message_type="message")
        message.save()
        to_user.new_notifications = True
        to_user.save()
        return render(request, 'notifications/message-sent.html', {
        })    
    else:
        return render(request, 'notifications/send-message.html', {
            'username':username,
        })    

def send_reply(request, subject_pk=0):
    if request.method == 'POST':
        title = request.POST.get('title')
        subject = Subject(pk = subject_pk)

        # hacky way to find out other guy's name
        # to_user = None
        for message in subject.messages.all():
            # If the message author is not me, then it's the other guy
            if message.from_user != request.user:
                to_user = message.from_user

        body = request.POST.get('body')
        message = Message(from_user=request.user,
                          to_user=to_user,
                          subject = subject,
                          body=body,
                          message_type="message")
        message.save()
        to_user.new_notifications = True
        to_user.save()
        
    return HttpResponseRedirect('/subject/'+str(subject_pk)+"/")
    
def subject(request, subject_pk=0):
    subject = Subject.objects.get(pk=subject_pk)
    messages = subject.messages.all().order_by('pub_date')


    return render(request, 'notifications/subject.html', {
        'subject':subject,
        'messages':messages,
    })    


def send_emails(request):
    teststring = send_email_notifications()    
    return render(request, 'posts/test.html', {
        'teststring': teststring,
    })    
