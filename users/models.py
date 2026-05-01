from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email      = models.EmailField(unique=True, verbose_name="E-posta Adresi")
    first_name = models.CharField(max_length=50, verbose_name="Ad")
    last_name  = models.CharField(max_length=50, verbose_name="Soyad")

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    @property
    def average_rating(self):
        """
        Kullanıcının aldığı tüm puanların ortalaması.
        reviews_received → ilanlar/models.py Review.target_user related_name'inden gelir.
        Veritabanı seviyesinde Avg() ile tek sorguda hesaplanır.
        """
        from django.db.models import Avg
        result = self.reviews_received.aggregate(ort=Avg('rating'))
        ort = result.get('ort')
        if ort is not None:
            return round(ort, 1)
        return 0

    def __str__(self):
        return self.username