from django.shortcuts import render

from .models import Message
# Create your views here.

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
