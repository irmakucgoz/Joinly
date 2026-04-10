from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Advertisement, Category
from .forms import AdvertisementForm
from django.db.models import Q
from django.contrib.auth import authenticate, login as auth_login, logout, get_user_model
from django.contrib import messages

def home(request):
    query = request.GET.get('q')
    categories = Category.objects.all()
    if query:
        ilanlar = Advertisement.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        ).distinct().order_by('-created_at')
    else:
        ilanlar = Advertisement.objects.all().order_by('-created_at')
    
    return render(request, 'index.html', {'ilanlar': ilanlar, 'query': query, 'categories': categories})

@login_required
def ilan_olustur(request):
    if request.method == 'POST':
        form = AdvertisementForm(request.POST)
        if form.is_valid():
            ilan = form.save(commit=False)
            ilan.owner = request.user
            ilan.save()
            return redirect('home') 
    else:
        form = AdvertisementForm()
    return render(request, 'ilanlar/ilan_form.html', {'form': form})

def ilan_detay(request, ilan_id):
    ilan = get_object_or_404(Advertisement, id=ilan_id)
    return render(request, 'ilanlar/ilan_detay.html', {'ilan': ilan})

@login_required
def ilan_duzenle(request, ilan_id):
    ilan = get_object_or_404(Advertisement, id=ilan_id, owner=request.user)
    if request.method == 'POST':
        form = AdvertisementForm(request.POST, instance=ilan)
        if form.is_valid():
            form.save()
            return redirect('ilan_detay', ilan_id=ilan.id)
    else:
        form = AdvertisementForm(instance=ilan)
    return render(request, 'ilanlar/ilan_form.html', {'form': form, 'title': 'İlanı Düzenle'})

@login_required
def ilan_sil(request, ilan_id):
    ilan = get_object_or_404(Advertisement, id=ilan_id, owner=request.user)
    if request.method == 'POST':
        ilan.delete()
        return redirect('home')
    return render(request, 'ilanlar/ilan_sil_onay.html', {'ilan': ilan})
@login_required
def profil_sayfasi(request):
    # Giriş yapmış kullanıcının kendi ilanlarını çekiyoruz
    kullanici_ilanlari = Advertisement.objects.filter(owner=request.user).order_by('-created_at')
    
    context = {
        'ilanlar': kullanici_ilanlari,
        'user': request.user
    }
    return render(request, 'users/profil.html', context)
def login_view(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        
        user = authenticate(username=u, password=p)
        
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Kullanıcı adı veya şifre hatalı!")
            
    return render(request, 'users/login.html')
User = get_user_model()
def register(request):
    if request.method == 'POST':
        # HTML'deki 'name' değerleriyle birebir aynı olmalı
        kadi = request.POST.get('username')
        ad = request.POST.get('first_name')
        soyad = request.POST.get('last_name')
        eposta = request.POST.get('email')
        sifre = request.POST.get('password')

        # Kullanıcı zaten var mı kontrolü
        if User.objects.filter(username=kadi).exists():
            messages.error(request, "Bu kullanıcı adı zaten alınmış!")
            return render(request, 'users/register.html')

        # Kullanıcıyı oluştur ve kaydet
        user = User.objects.create_user(
            username=kadi,
            first_name=ad,
            last_name=soyad,
            email=eposta,
            password=sifre
        )
        
        auth_login(request, user)
        messages.success(request, "Aramıza hoş geldin!")
        return redirect('home')

    return render(request, 'users/register.html')
def logout_view(request):
    logout(request)
    messages.success(request, "Başarıyla çıkış yaptınız. Yine bekleriz!")
    return redirect('home')

