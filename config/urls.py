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
from django.urls import path, include # 1. BURAYA 'include' EKLEDİK
from ilanlar.views import index , ilan_olustur , ilan_detay , ilan_duzenle , ilan_sil

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 2. SENİN EKLEYECEĞİN SATIR TAM OLARAK BURASI:
    path('users/', include('users.urls')), 
    path('', index, name='home'),
    path('yeni-ilan/', ilan_olustur, name='ilan_olustur'),
    path('ilan/<int:ilan_id>/', ilan_detay, name='ilan_detay'),
    # config/urls.py içindeki urlpatterns listesine ekle:
    path('ilan/<int:ilan_id>/duzenle/', ilan_duzenle, name='ilan_duzenle'),
    path('ilan/<int:ilan_id>/sil/', ilan_sil, name='ilan_sil'),
    # Eğer ilanlar uygulaman hazırsa onu da buraya bağlayabilirsin:
    # path('', include('ilanlar.urls')), 
]