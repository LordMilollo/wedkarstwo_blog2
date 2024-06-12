import locale
import pytz
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, Post, Komentarz
from django.conf import settings
from django.utils import timezone

# Ustawienie lokalizacji na polski dla Windowsa
locale.setlocale(locale.LC_TIME, 'Polish_Poland.1250')

# Wyrejestrowanie modelu Group, jeśli nie jest potrzebny
admin.site.unregister(Group)

def format_datetime(dt):
    if dt:
        local_tz = pytz.timezone(settings.TIME_ZONE)
        local_dt = dt.astimezone(local_tz)
        return local_dt.strftime('%d-%m-%Y %H:%M')
    return ''

class CustomUserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Informacje personalne'), {'fields': ('first_name', 'last_name', 'email', 'imie', 'nazwisko', 'wiek')}),
        (_('Uprawnienia'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (_('Ważne daty'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'imie', 'nazwisko', 'wiek', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)

class PostAdmin(admin.ModelAdmin):
    list_display = ('tytul', 'autor', 'data_publikacji_formatted')
    search_fields = ('tytul', 'autor__username')
    list_filter = ('data_publikacji',)
    ordering = ['-data_publikacji']

    def data_publikacji_formatted(self, obj):
        return format_datetime(obj.data_publikacji)

    data_publikacji_formatted.admin_order_field = 'data_publikacji'
    data_publikacji_formatted.short_description = 'Data publikacji'

class KomentarzAdmin(admin.ModelAdmin):
    list_display = ('post', 'autor', 'data_publikacji_formatted')
    search_fields = ('post__tytul', 'autor__username')
    list_filter = ('data_publikacji',)
    ordering = ['-data_publikacji']

    def data_publikacji_formatted(self, obj):
        return format_datetime(obj.data_publikacji)

    data_publikacji_formatted.admin_order_field = 'data_publikacji'
    data_publikacji_formatted.short_description = 'Data publikacji'

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Komentarz, KomentarzAdmin)

# Zmiana nagłówka strony administracyjnej
admin.site.site_header = "Panel Administracyjny Blogu Wędkarskiego"
admin.site.site_title = "Panel Administracyjny"
admin.site.index_title = "Zarządzaj Blogiem Wędkarskim"
