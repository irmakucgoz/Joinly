from django.conf import settings
from django.db import models

class Category(models.Model):
    name  = models.CharField(max_length=50, verbose_name='Kategori Adı')
    color = models.CharField(max_length=7, default='#007bff', verbose_name='Kategori Rengi')

    class Meta:
        verbose_name_plural = 'Kategoriler'

    def __str__(self):
        return self.name

class Advertisement(models.Model):
    owner       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category    = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='ilanlar')
    title       = models.CharField(max_length=200, verbose_name='İlan Başlığı')
    description = models.TextField(verbose_name='Açıklama')
    location    = models.CharField(max_length=100, verbose_name='Konum')
    
    
    latitude    = models.FloatField(verbose_name='Enlem', null=True, blank=True)
    longitude   = models.FloatField(verbose_name='Boylam', null=True, blank=True)
    
    created_at  = models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')

    def __str__(self):
        return self.title


class Conversation(models.Model):
    ad = models.ForeignKey(Advertisement, on_delete=models.CASCADE, related_name='conversations')
    participant1 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='conversations_started', on_delete=models.CASCADE)
    participant2 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='conversations_received', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('ad', 'participant1', 'participant2')
        ordering = ['-updated_at']

    def __str__(self):
        return f"Konuşma ID: {self.id} | {self.participant1.username} & {self.participant2.username}"


class Message(models.Model):
    # Eski 'receiver' ve 'ad' silindi, yerine 'conversation' geldi.
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    sender       = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_messages', on_delete=models.CASCADE)
    content      = models.TextField(verbose_name='Mesaj İçeriği')
    sent_at      = models.DateTimeField(auto_now_add=True)
    is_read      = models.BooleanField(default=False, verbose_name='Okundu mu?')

    class Meta:
        ordering = ['sent_at']

    def __str__(self):
        return f'{self.sender.username}: {self.content[:20]}...'

class Review(models.Model):
    reviewer    = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reviews_made',     on_delete=models.CASCADE)
    target_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reviews_received', on_delete=models.CASCADE)
    rating      = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)], verbose_name='Puan')
    comment     = models.TextField(verbose_name='Yorum')
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('reviewer', 'target_user')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.reviewer} → {self.target_user} ({self.rating}/5)'


class Favorite(models.Model):
    
    user       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favoriler')
    ad         = models.ForeignKey(Advertisement, on_delete=models.CASCADE, related_name='favoriler')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'ad')
        ordering        = ['-created_at']
        verbose_name        = 'Favori'
        verbose_name_plural = 'Favoriler'

    def __str__(self):
        return f'{self.user.username} ♥ {self.ad.title}'
