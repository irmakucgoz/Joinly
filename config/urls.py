"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from ilanlar.views import index, ilan_olustur, ilan_detay, ilan_duzenle, ilan_sil, profil_sayfasi

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Kullanıcı işlemleri (Kayıt, Giriş vb.)
    path('users/', include('users.urls')), 
    
    # İlan İşlemleri
    # NOT: 'name' kısmını 'index' yaptık ki HTML'deki {% url 'index' %} kodu çalışsın.
    path('', index, name='home'), 
    path('yeni-ilan/', ilan_olustur, name='ilan_olustur'),
    path('ilan/<int:ilan_id>/', ilan_detay, name='ilan_detay'),
    path('ilan/<int:ilan_id>/duzenle/', ilan_duzenle, name='ilan_duzenle'),
    path('ilan/<int:ilan_id>/sil/', ilan_sil, name='ilan_sil'),
    path('profil/', profil_sayfasi, name='profil'),
]