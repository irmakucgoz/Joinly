from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.home, name='home'),
    
    
    path('ilan/<int:ilan_id>/', views.ilan_detay, name='ilan_detay'),
    
    
    path('yeni-ilan/', views.ilan_olustur, name='ilan_olustur'),
    
    
    path('ilan/<int:ilan_id>/duzenle/', views.ilan_duzenle, name='ilan_duzenle'),
    
    
    path('ilan/<int:ilan_id>/sil/', views.ilan_sil, name='ilan_sil'),
]