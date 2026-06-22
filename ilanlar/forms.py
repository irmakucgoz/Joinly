from django import forms
from .models import Advertisement

class AdvertisementForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        
        fields = ['title', 'category', 'description', 'location', 'latitude', 'longitude']
        
        
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Örn: Matematik Çalışma Grubu'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control', 
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 4,
                'placeholder': 'Hangi konularda çalışacağız? Saat kaçta?'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Örn: Haritadan seçin veya adres yazın...',
                'id': 'map-search-input' 
            }),
            
            'latitude': forms.HiddenInput(attrs={'id': 'id_latitude'}),
            'longitude': forms.HiddenInput(attrs={'id': 'id_longitude'}),
        }
