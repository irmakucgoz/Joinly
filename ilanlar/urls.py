from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    
    
    path('ilan/<int:ilan_id>/', views.ilan_detay, name='ilan_detay'),
    
    path('yeni-ilan/', views.ilan_olustur, name='ilan_olustur'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    
    path('register/', views.register, name='register'),
    
    path('profil/', views.profil_sayfasi, name='profil'),
]