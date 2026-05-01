from .models import Message

def unread_messages_count(request):
    if request.user.is_authenticated:
        # 'recipient' yerine 'receiver' yazıyoruz çünkü modelinde öyle tanımlı
        count = Message.objects.filter(receiver=request.user, is_read=False).count()
        return {'unread_count': count}
    return {'unread_count': 0}