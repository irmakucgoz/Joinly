from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from .models import Advertisement, Category, Message, Review, Favorite
from .forms import AdvertisementForm


def home(request):
    query      = request.GET.get('q', '').strip()
    kategori   = request.GET.get('kategori', '')
    konum      = request.GET.get('konum', '').strip()
    siralama   = request.GET.get('siralama', 'yeni')
    
    categories = Category.objects.all()

    ilanlar = Advertisement.objects.select_related('owner', 'category')

    if query:
        ilanlar = ilanlar.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

    if kategori:
        ilanlar = ilanlar.filter(category__id=kategori)

    if konum:
        ilanlar = ilanlar.filter(location__icontains=konum)

    if siralama == 'eski':
        ilanlar = ilanlar.order_by('created_at')
    elif siralama == 'a_z':
        ilanlar = ilanlar.order_by('title')
    elif siralama == 'z_a':
        ilanlar = ilanlar.order_by('-title')
    else:
        ilanlar = ilanlar.order_by('-created_at')

    # Giriş yapmış kullanıcının favori ilan id'lerini bir küme olarak al
    favori_ilan_idleri = set()
    if request.user.is_authenticated:
        favori_ilan_idleri = set(
            Favorite.objects.filter(user=request.user).values_list('ad_id', flat=True)
        )

    context = {
        'ilanlar'          : ilanlar,
        'query'            : query,
        'categories'       : categories,
        'secili_kategori'  : kategori,
        'secili_konum'     : konum,
        'secili_siralama'  : siralama,
        'favori_ilan_idleri': favori_ilan_idleri,
    }
    return render(request, 'index.html', context)


def ilan_detay(request, ilan_id):
    ilan = get_object_or_404(Advertisement, id=ilan_id)

    # Bu ilanın kullanıcının favorisinde olup olmadığını kontrol et
    is_favori = False
    if request.user.is_authenticated:
        is_favori = Favorite.objects.filter(user=request.user, ad=ilan).exists()

    return render(request, 'ilanlar/ilan_detay.html', {
        'ilan': ilan,
        'is_favori': is_favori,
    })


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
# YENİ: FAVORİLEME VIEW'LARI
# ─────────────────────────────────────────

@login_required
def favori_toggle(request, ilan_id):
    """
    POST isteği ile ilanı favorilere ekler veya çıkarır.
    AJAX ve normal form POST'larını destekler.
    Durum: {'is_favori': True/False, 'favori_sayisi': int}
    """
    if request.method != 'POST':
        return redirect('ilan_detay', ilan_id=ilan_id)

    ilan = get_object_or_404(Advertisement, id=ilan_id)

    favori, created = Favorite.objects.get_or_create(user=request.user, ad=ilan)

    if not created:
        # Zaten favorilerdeydi → çıkar
        favori.delete()
        is_favori = False
    else:
        # Yeni eklendi
        is_favori = True

    # AJAX isteği ise JSON döndür
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'is_favori'    : is_favori,
            'favori_sayisi': ilan.favoriler.count(),
        })

    # Normal form POST ise ilan detayına geri dön
    return redirect('ilan_detay', ilan_id=ilan_id)


@login_required
def favorilerim(request):
    """
    Giriş yapmış kullanıcının kaydettiği tüm ilanları listeler.
    """
    favori_kayitlar = (
        Favorite.objects
        .filter(user=request.user)
        .select_related('ad', 'ad__owner', 'ad__category')
        .order_by('-created_at')
    )
    return render(request, 'ilanlar/favorilerim.html', {
        'favori_kayitlar': favori_kayitlar,
    })


# ─────────────────────────────────────────
# MESAJLAŞMA VIEW'LARI
# ─────────────────────────────────────────

@login_required
def mesaj_gonder(request, ilan_id):
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
    tum_mesajlar = Message.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user)
    ).select_related('sender', 'receiver', 'ad').order_by('-sent_at')

    konusmalar = {}
    for mesaj in tum_mesajlar:
        diger   = mesaj.receiver if mesaj.sender == request.user else mesaj.sender
        anahtar = (diger.id, mesaj.ad.id)

        if anahtar not in konusmalar:
            konusmalar[anahtar] = {
                'diger_kullanici': diger,
                'ilan'           : mesaj.ad,
                'son_mesaj'      : mesaj,
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
    from django.http import HttpResponseForbidden
    from django.contrib.auth import get_user_model
    User = get_user_model()

    diger_kullanici = get_object_or_404(User, id=diger_kullanici_id)
    ilan            = get_object_or_404(Advertisement, id=ilan_id)

    konusma_taraflari = {ilan.owner.id, diger_kullanici.id}
    if request.user.id not in konusma_taraflari:
        return HttpResponseForbidden(
            '<h2>Bu konuşmaya erişim yetkin yok.</h2>'
            '<p><a href="/">Ana Sayfaya Dön</a></p>'
        )

    konusma_mesajlari = Message.objects.filter(
        ad=ilan,
    ).filter(
        Q(sender=ilan.owner, receiver=diger_kullanici) |
        Q(sender=diger_kullanici, receiver=ilan.owner)
    ).order_by('sent_at')

    konusma_mesajlari.filter(
        receiver=request.user,
        is_read=False,
    ).update(is_read=True)

    if request.method == 'POST':
        icerik = request.POST.get('icerik', '').strip()
        if icerik:
            alici = diger_kullanici if request.user == ilan.owner else ilan.owner
            Message.objects.create(
                sender=request.user,
                receiver=alici,
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


# ─────────────────────────────────────────
# PUANLAMA SİSTEMİ VIEW'I
# ─────────────────────────────────────────

@login_required
def kullanici_puanla(request, hedef_kullanici_id):
    from django.contrib.auth import get_user_model
    User        = get_user_model()
    target_user = get_object_or_404(User, id=hedef_kullanici_id)

    next_url = request.POST.get('next') or request.GET.get('next', '')

    if request.method == 'POST':
        if request.user == target_user:
            messages.error(request, 'Kendine puan veremezsin!')
            if next_url:
                return redirect(next_url)
            return redirect('kullanici_profil', kullanici_id=target_user.id)

        puan  = request.POST.get('rating', '').strip()
        yorum = request.POST.get('comment', '').strip()

        if not puan:
            messages.error(request, 'Lütfen bir puan seç.')
            if next_url:
                return redirect(next_url)
            return redirect('kullanici_profil', kullanici_id=target_user.id)

        Review.objects.update_or_create(
            reviewer=request.user,
            target_user=target_user,
            defaults={'rating': int(puan), 'comment': yorum},
        )
        messages.success(request, f'{target_user.username} adlı kullanıcıya puanın iletildi!')

    if next_url:
        return redirect(next_url)
    return redirect('kullanici_profil', kullanici_id=target_user.id)