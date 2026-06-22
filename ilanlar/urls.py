from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('ilan/<int:ilan_id>/', views.ilan_detay, name='ilan_detay'),
    path('yeni-ilan/', views.ilan_olustur, name='ilan_olustur'),
    path('ilan/<int:ilan_id>/duzenle/', views.ilan_duzenle, name='ilan_duzenle'),
    path('ilan/<int:ilan_id>/sil/', views.ilan_sil, name='ilan_sil'),

    
    path('ilan/<int:ilan_id>/mesaj-gonder/', views.mesaj_gonder, name='mesaj_gonder'),
    path('mesajlar/', views.gelen_kutusu, name='gelen_kutusu'),
    
    
    path('mesajlar/<int:conversation_id>/', views.konusma_detay, name='konusma_detay'),

    
    path('puanla/<int:hedef_kullanici_id>/', views.kullanici_puanla, name='kullanici_puanla'),

    
    path('ilan/<int:ilan_id>/favori/', views.favori_toggle, name='favori_toggle'),
    path('favorilerim/', views.favorilerim, name='favorilerim'),
]
