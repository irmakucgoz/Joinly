from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Max
from .models import Advertisement, Category, Message
from .forms import AdvertisementForm


def home(request):
    query      = request.GET.get('q', '').strip()
    kategori   = request.GET.get('kategori', '')
    categories = Category.objects.all()

    ilanlar = Advertisement.objects.select_related('owner', 'category').order_by('-created_at')

    if query:
        ilanlar = ilanlar.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

    if kategori:
        ilanlar = ilanlar.filter(category__id=kategori)

    context = {
        'ilanlar'        : ilanlar,
        'query'          : query,
        'categories'     : categories,
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


# ─────────────────────────────────────────
# MESAJLAŞMA VIEW'LARI
# ─────────────────────────────────────────

@login_required
def mesaj_gonder(request, ilan_id):
    """
    Bir ilana tıklayıp 'Mesaj Gönder' diyen kullanıcı buraya gelir.
    İlan sahibine mesaj gönderir.
    Kendi ilanına mesaj gönderemez.
    """
    ilan = get_object_or_404(Advertisement, id=ilan_id)

    
    if ilan.owner == request.user:
        messages.error(request, 'Kendi ilanına mesaj gönderemezsin.')
        return redirect('ilan_detay', ilan_id=ilan_id)

    if request.method == 'POST':
        icerik = request.POST.get('icerik', '').strip()

        if not icerik:
            messages.error(request, 'Mesaj boş olamaz.')
            return redirect('ilan_detay', ilan_id=ilan_id)

        Message.objects.create(
            sender=request.user,
            receiver=ilan.owner,
            ad=ilan,
            content=icerik,
        )
        messages.success(request, f'{ilan.owner.first_name} adlı kullanıcıya mesajın gönderildi!')
        
        return redirect('konusma_detay', diger_kullanici_id=ilan.owner.id, ilan_id=ilan.id)

    
    return redirect('ilan_detay', ilan_id=ilan_id)


@login_required
def gelen_kutusu(request):
    """
    Kullanıcının tüm konuşmalarını listeler.
    Her konuşma: (diğer kullanıcı + ilan) çifti olarak gruplanır.
    En son mesaj öne çıkar.
    """
    
    tum_mesajlar = Message.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user)
    ).select_related('sender', 'receiver', 'ad').order_by('-sent_at')

    
    konusmalar = {}
    for mesaj in tum_mesajlar:
        
        diger = mesaj.receiver if mesaj.sender == request.user else mesaj.sender
        anahtar = (diger.id, mesaj.ad.id)

        if anahtar not in konusmalar:
            konusmalar[anahtar] = {
                'diger_kullanici': diger,
                'ilan'           : mesaj.ad,
                'son_mesaj'      : mesaj,
                # Okunmamış mesaj var mı? (bana gelen, henüz görülmemiş)
                'okunmamis'      : Message.objects.filter(
                    sender=diger,
                    receiver=request.user,
                    ad=mesaj.ad,
                    is_read=False,
                ).exists(),
            }

    context = {
        'konusmalar': list(konusmalar.values()),
    }
    return render(request, 'ilanlar/gelen_kutusu.html', context)


@login_required
def konusma_detay(request, diger_kullanici_id, ilan_id):
    """
    İki kullanıcı arasındaki, belirli bir ilana ait konuşmanın tüm mesajlarını gösterir.
    Yeni mesaj göndermek için POST kabul eder.
    Sayfaya girince okunmamış mesajları 'okundu' olarak işaretler.
    """
    from django.contrib.auth import get_user_model
    User = get_user_model()

    diger_kullanici = get_object_or_404(User, id=diger_kullanici_id)
    ilan            = get_object_or_404(Advertisement, id=ilan_id)

    
    
    yetkili = (
        request.user == ilan.owner or
        request.user == diger_kullanici
    )
    if not yetkili:
        messages.error(request, 'Bu konuşmaya erişim yetkin yok.')
        return redirect('gelen_kutusu')

    
    konusma_mesajlari = Message.objects.filter(
        ad=ilan,
    ).filter(
        Q(sender=request.user, receiver=diger_kullanici) |
        Q(sender=diger_kullanici, receiver=request.user)
    ).order_by('sent_at')

    
    konusma_mesajlari.filter(
        receiver=request.user,
        is_read=False,
    ).update(is_read=True)

    
    if request.method == 'POST':
        icerik = request.POST.get('icerik', '').strip()
        if icerik:
            Message.objects.create(
                sender=request.user,
                receiver=diger_kullanici,
                ad=ilan,
                content=icerik,
            )
        return redirect('konusma_detay', diger_kullanici_id=diger_kullanici_id, ilan_id=ilan_id)

    context = {
        'diger_kullanici'  : diger_kullanici,
        'ilan'             : ilan,
        'konusma_mesajlari': konusma_mesajlari,
    }
    return render(request, 'ilanlar/konusma_detay.html', context)