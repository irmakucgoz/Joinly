from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Analiz: Email benzersiz olmalı 
    email = models.EmailField(unique=True, verbose_name="E-posta Adresi")
    
    # Analiz: Ad ve Soyad alanları [cite: 7]
    first_name = models.CharField(max_length=50, verbose_name="Ad")
    last_name = models.CharField(max_length=50, verbose_name="Soyad")

    # Analiz: Giriş yaparken email kullanmak için (Gereksinim 24) 
    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.username