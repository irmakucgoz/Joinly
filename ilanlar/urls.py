from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('ilan/<int:pk>/', views.ilan_detay, name='ilan_detay'),
    path('yeni-ilan/', views.ilan_olustur, name='ilan_olustur'),
    path('profil/', views.profil_sayfasi, name='profil'),
]