from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # Listede hangi başlıklar görünsün?
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff']
    
    # Standart şifre ve kullanıcı ayarlarını kullan
    fieldsets = UserAdmin.fieldsets 
    add_fieldsets = UserAdmin.add_fieldsets

# Sadece bu satırı bırakıyoruz, unregister satırını tamamen sildik!
admin.site.register(CustomUser, CustomUserAdmin)