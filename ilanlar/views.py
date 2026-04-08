from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Advertisement
from .forms import AdvertisementForm
from django.db.models import Q

def index(request):
    query = request.GET.get('q')
    if query:
        ilanlar = Advertisement.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        ).distinct().order_by('-created_at')
    else:
        ilanlar = Advertisement.objects.all().order_by('-created_at')
    
    return render(request, 'index.html', {'ilanlar': ilanlar, 'query': query})

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