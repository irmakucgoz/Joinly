from django.shortcuts import render , redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Advertisement
from .forms import AdvertisementForm
from django.db.models import Q

def index(request):
    # Veritabanındaki tüm ilanları çekiyoruz
    ilanlar = Advertisement.objects.all().order_by('-created_at')
    
    # Bu ilanları index.html sayfasına paketleyip gönderiyoruz
    context = {
        'ilanlar': ilanlar
    }
    return render(request, 'index.html', context)

@login_required # Giriş yapmamış olanı login'e fırlatır
def ilan_olustur(request):
    if request.method == 'POST':
        form = AdvertisementForm(request.POST)
        if form.is_valid():
            ilan = form.save(commit=False)
            ilan.owner = request.user # İlanın sahibi o anki kullanıcı olsun
            ilan.save()
            return redirect('home')
    else:
        form = AdvertisementForm()
    
    return render(request, 'ilanlar/ilan_form.html', {'form': form})
def ilan_detay(request, ilan_id):
    ilan = Advertisement.objects.get(id=ilan_id)
    return render(request, 'ilanlar/ilan_detay.html', {'ilan': ilan})

from django.shortcuts import get_object_or_404

# DÜZENLEME (Update)
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

# SİLME (Delete)
@login_required
def ilan_sil(request, ilan_id):
    ilan = get_object_or_404(Advertisement, id=ilan_id, owner=request.user)
    if request.method == 'POST': # Güvenlik için sadece POST ile sileriz
        ilan.delete()
        return redirect('home')
    return render(request, 'ilanlar/ilan_sil_onay.html', {'ilan': ilan})
    def index(request):
        query = request.GET.get('q') # URL'den 'q' parametresini (arama kelimesini) al
        if query:
        # Eğer arama yapılmışsa, başlıkta VEYA açıklamada geçenleri filtrele
            ilanlar = Advertisement.objects.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            ).distinct()
        else:
        # Arama yoksa tüm ilanları getir
            ilanlar = Advertisement.objects.all().order_by('-created_at')
    
    return render(request, 'ilanlar/index.html', {'ilanlar': ilanlar, 'query': query})