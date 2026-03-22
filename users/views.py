from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages # Hata mesajları için (Analiz madde 26)

def login_view(request):
    # Eğer kullanıcı zaten giriş yapmışsa direkt ana sayfaya gönder
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        # DİKKAT: Burada 'email' yerine 'username' almalıyız
        username_data = request.POST.get('username') 
        password_data = request.POST.get('password')

        # 1. Kontrol: Boş bırakılamaz
        if not username_data or not password_data:
            messages.error(request, "Lütfen tüm alanları doldurun.")
            return render(request, 'users/login.html')

        # 2. Kontrol: Django'nun standart authenticate fonksiyonu 'username' bekler
        user = authenticate(request, username=username_data, password=password_data)

        if user is not None:
            login(request, user) 
            return redirect('home') 
        else:
            messages.error(request, "Kullanıcı adı veya şifre hatalı!")
    
    return render(request, 'users/login.html')

def logout_view(request):
    logout(request) # Session çerezlerini temizle [cite: 57, 60]
    return redirect('home') # Misafir olarak ana sayfaya gönder [cite: 60]

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CustomUser # Bizim oluşturduğumuz özel kullanıcı modeli [cite: 12]

def register_view(request):
    if request.method == 'POST':
        # UI'dan gelen verileri kutulara koyuyoruz [cite: 7, 11]
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # 1. Kontrol: Şifre en az 8 karakter mi? [cite: 8]
        if len(password) < 8:
            messages.error(request, "Şifre en az 8 karakterden oluşmalı!")
            return render(request, 'users/register.html')

        # 2. Kontrol: Email daha önce alınmış mı? [cite: 14]
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Bu e-posta adresiyle zaten bir hesap var!") 
            return render(request, 'users/register.html')

        # 3. Kontrol: Kullanıcı adı daha önce alınmış mı? [cite: 7]
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Bu kullanıcı adı zaten alınmış!")
            return render(request, 'users/register.html')

        # Her şey yolundaysa kullanıcıyı oluştur ve ŞİFREYİ HASHLE 
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        user.save() # Veritabanına aktar 

        messages.success(request, "Kayıt başarılı! Giriş yapabilirsiniz.")
        return redirect('login') # Başarılıysa login sayfasına yönlendir 

    return render(request, 'users/register.html')