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
    
    path('mesajlar/<int:diger_kullanici_id>/<int:ilan_id>/', views.konusma_detay, name='konusma_detay'),
]