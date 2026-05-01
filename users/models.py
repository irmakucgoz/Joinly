from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="E-posta Adresi")
    first_name = models.CharField(max_length=50, verbose_name="Ad")
    last_name = models.CharField(max_length=50, verbose_name="Soyad")

    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    @property
    def average_rating(self):
        """
        Kullanıcının aldığı tüm puanların aritmetik ortalamasını hesaplar.
        'reviews_received' alanı ilanlar/models.py'daki related_name'den beslenir.
        """
        ratings = self.reviews_received.all()
        if ratings.exists():
            # Tüm puanları toplayıp toplam sayıya bölüyoruz
            total = sum([r.rating for r in ratings])
            return round(total / ratings.count(), 1)
        return 0

    def __str__(self):
        return self.username