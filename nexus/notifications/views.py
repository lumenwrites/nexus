from django.shortcuts import render
from django.http import HttpResponseRedirect

from .models import Notification
from profiles.models import User
from .utils import send_email_notifications

def notifications(request):
    if request.user.new_notifications:
        notifications = Notification.objects.filter(to_user=request.user,
                                                     isread=False).order_by('-pub_date')
        for notification in notifications:
            notification.isread = True
            notification.save()
        user = request.user
        user.new_notifications = False
        user.save()
    else:
        # Old notifications
        notifications = Notification.objects.filter(to_user=request.user).order_by('-pub_date')
    
    return render(request, 'notifications/notifications.html', {
        'notifications':notifications,
    })



def send_emails(request):
    teststring = send_email_notifications()    
    return render(request, 'posts/test.html', {
        'teststring': teststring,
    })    
