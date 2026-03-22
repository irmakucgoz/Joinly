from django.contrib import admin
from .models import Category, Advertisement, Message, Review

admin.site.register(Category)
admin.site.register(Advertisement)
admin.site.register(Message)
admin.site.register(Review)