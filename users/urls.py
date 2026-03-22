from django.urls import path
from .views import login_view, logout_view, register_view # 1. BURAYA 'register_view' EKLEDİK

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    
    # 2. EKSİK OLAN KRİTİK SATIR TAM OLARAK BU:
    path('register/', register_view, name='register'), 
]