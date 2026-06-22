from django.db.models import Q
from .models import Message

def unread_messages_count(request):
    if request.user.is_authenticated:
    
        count = Message.objects.filter(
            Q(conversation__participant1=request.user) | Q(conversation__participant2=request.user),
            is_read=False
        ).exclude(sender=request.user).count()
        return {'unread_count': count}
    
    return {'unread_count': 0}
