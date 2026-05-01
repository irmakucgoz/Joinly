from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Kullanıcı işlemleri (kayıt, giriş, çıkış, profil)
    # users/urls.py dosyasına yönlendir
    path('', include('users.urls')),
    
    # İlan işlemleri (ana sayfa, ilan detay, yeni ilan vs.)
    # ilanlar/urls.py dosyasına yönlendir
    path('', include('ilanlar.urls')),
]