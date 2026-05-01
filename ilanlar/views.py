from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Advertisement, Category
from .forms import AdvertisementForm


def home(request):
    query      = request.GET.get('q', '').strip()
    kategori   = request.GET.get('kategori', '')
    categories = Category.objects.all()

    ilanlar = Advertisement.objects.select_related('owner', 'category').order_by('-created_at')

    # Metin araması
    if query:
        ilanlar = ilanlar.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

    # Kategori filtresi
    if kategori:
        ilanlar = ilanlar.filter(category__id=kategori)

    context = {
        'ilanlar'   : ilanlar,
        'query'     : query,
        'categories': categories,
        'secili_kategori': kategori,
    }
    return render(request, 'index.html', context)


def ilan_detay(request, ilan_id):
    ilan = get_object_or_404(Advertisement, id=ilan_id)
    return render(request, 'ilanlar/ilan_detay.html', {'ilan': ilan})


@login_required
def ilan_olustur(request):
    if request.method == 'POST':
        form = AdvertisementForm(request.POST)
        if form.is_valid():
            ilan = form.save(commit=False)
            ilan.owner = request.user   
            ilan.save()
            messages.success(request, 'İlanın başarıyla yayınlandı!')
            return redirect('ilan_detay', ilan_id=ilan.id)
    else:
        form = AdvertisementForm()

    return render(request, 'ilanlar/ilan_form.html', {'form': form, 'baslik': 'Yeni İlan Oluştur'})


@login_required
def ilan_duzenle(request, ilan_id):
    
    ilan = get_object_or_404(Advertisement, id=ilan_id, owner=request.user)

    if request.method == 'POST':
        form = AdvertisementForm(request.POST, instance=ilan)
        if form.is_valid():
            form.save()
            messages.success(request, 'İlan başarıyla güncellendi.')
            return redirect('ilan_detay', ilan_id=ilan.id)
    else:
        form = AdvertisementForm(instance=ilan)

    return render(request, 'ilanlar/ilan_form.html', {'form': form, 'baslik': 'İlanı Düzenle'})


@login_required
def ilan_sil(request, ilan_id):
    ilan = get_object_or_404(Advertisement, id=ilan_id, owner=request.user)

    if request.method == 'POST':
        ilan.delete()
        messages.success(request, 'İlan silindi.')
        return redirect('home')

    return render(request, 'ilanlar/ilan_sil_onay.html', {'ilan': ilan})