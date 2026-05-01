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
    created_at  = models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')

    def __str__(self):
        return self.title


class Message(models.Model):
    sender   = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_messages',     on_delete=models.CASCADE)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_messages', on_delete=models.CASCADE)
    ad       = models.ForeignKey(Advertisement, on_delete=models.CASCADE, related_name='mesajlar')
    content  = models.TextField(verbose_name='Mesaj İçeriği')
    sent_at  = models.DateTimeField(auto_now_add=True)

    # YENİ: Mesaj okundu mu?
    is_read  = models.BooleanField(default=False, verbose_name='Okundu mu?')

    def __str__(self):
        return f'{self.sender} → {self.receiver} | {self.ad.title}'


class Review(models.Model):
    reviewer    = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reviews_made',     on_delete=models.CASCADE)
    target_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reviews_received', on_delete=models.CASCADE)
    rating      = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)], verbose_name='Puan')
    comment     = models.TextField(verbose_name='Yorum')
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.reviewer} → {self.target_user} ({self.rating}/5)'