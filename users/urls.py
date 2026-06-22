# users/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('kayit/',                     views.register_view,    name='register'),
    path('giris/',                     views.login_view,       name='login'),
    path('cikis/',                     views.logout_view,      name='logout'),
    path('profil/',                    views.profil_sayfasi,   name='profil'),
    
    path('kullanici/<int:kullanici_id>/', views.kullanici_profil, name='kullanici_profil'),
]
