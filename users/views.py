from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import CustomUser


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username   = request.POST.get('username', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name  = request.POST.get('last_name', '').strip()
        email      = request.POST.get('email', '').strip()
        password   = request.POST.get('password', '')

        if not all([username, first_name, last_name, email, password]):
            messages.error(request, 'Lütfen tüm alanları doldurun.')
            return render(request, 'users/register.html')

        if len(password) < 8:
            messages.error(request, 'Şifre en az 8 karakter olmalıdır.')
            return render(request, 'users/register.html')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Bu kullanıcı adı zaten alınmış.')
            return render(request, 'users/register.html')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Bu e-posta adresiyle zaten bir hesap var.')
            return render(request, 'users/register.html')

        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

        login(request, user)
        messages.success(request, f'Hoş geldin, {first_name}! Hesabın oluşturuldu.')
        return redirect('home')

    return render(request, 'users/register.html')


def login_view(request):
    
    storage = messages.get_messages(request)
    for _ in storage:
        pass

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        if not username or not password:
            messages.error(request, 'Lütfen tüm alanları doldurun.')
            return render(request, 'users/login.html')

        try:
            user_obj = CustomUser.objects.get(username=username)
            user = authenticate(request, username=user_obj.email, password=password)
        except CustomUser.DoesNotExist:
            user = None

        if user is not None:
            login(request, user)
            messages.success(request, f'Tekrar hoş geldin, {user.first_name}!')
            return redirect('home')
        else:
            messages.error(request, 'Kullanıcı adı veya şifre hatalı.')

    return render(request, 'users/login.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'Başarıyla çıkış yaptınız.')
    return redirect('home')


@login_required
def profil_sayfasi(request):
    
    from ilanlar.models import Advertisement
    kullanici_ilanlari = Advertisement.objects.filter(
        owner=request.user
    ).order_by('-created_at')

    context = {
        'profile_user': request.user,
        'ilanlar'     : kullanici_ilanlari,
    }
    return render(request, 'users/profil.html', context)


def kullanici_profil(request, kullanici_id):
    
    from ilanlar.models import Advertisement
    profile_user       = get_object_or_404(CustomUser, id=kullanici_id)
    kullanici_ilanlari = Advertisement.objects.filter(
        owner=profile_user
    ).order_by('-created_at')

    context = {
        'profile_user': profile_user,
        'ilanlar'     : kullanici_ilanlari,
    }
    return render(request, 'users/profil.html', context)
