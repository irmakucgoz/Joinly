from django import forms
from .models import Advertisement

class AdvertisementForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        # Harita koordinatları için latitude ve longitude alanlarını da forma dahil ettik
        fields = ['title', 'category', 'description', 'location', 'latitude', 'longitude']
        
        # TASARIM BURADA BAŞLIYOR: Her kutuya o 'form-control' stilini veriyoruz
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control', # Mor ve köşeli tasarım
                'placeholder': 'Örn: Matematik Çalışma Grubu'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control', # Açılır liste için aynı stil
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control', # Büyük yazı alanı için aynı stil
                'rows': 4,
                'placeholder': 'Hangi konularda çalışacağız? Saat kaçta?'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Örn: Haritadan seçin veya adres yazın...',
                'id': 'map-search-input' # Google Haritalar API'si (Autocomplete) bu ID'yi kullanacak
            }),
            # Kullanıcı enlem ve boylamı elle girmeyecek, haritadan otomatik gelecek
            # Bu yüzden bunları formda görünmez yapıyoruz.
            'latitude': forms.HiddenInput(attrs={'id': 'id_latitude'}),
            'longitude': forms.HiddenInput(attrs={'id': 'id_longitude'}),
        }