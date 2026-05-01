# users/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('kayit/',                    views.register_view,   name='register'),
    path('giris/',                    views.login_view,      name='login'),
    path('cikis/',                    views.logout_view,     name='logout'),
    path('profil/',                   views.profil_sayfasi,  name='profil'),
    # Herkese açık profil sayfası — puanlama formu buraya yönlenir
    path('profil/<int:kullanici_id>/', views.kullanici_profil, name='kullanici_profil'),
]