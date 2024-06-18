from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Customer, Charge, Boleto

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'cpf', 'birth_date', 'phone_number')
    search_fields = ('user__username', 'cpf', 'phone_number')

@admin.register(Charge)
class ChargeAdmin(admin.ModelAdmin):
    list_display = ('customer', 'value', 'description', 'created_at')
    search_fields = ('customer__user__username', 'description')
    list_filter = ('created_at',)

@admin.register(Boleto)
class BoletoAdmin(admin.ModelAdmin):
    list_display = ('charge', 'expire_at', 'barcode', 'pdf', 'status', 'qrcode', 'pix_key')
    search_fields = ('charge__customer__user__username', 'barcode', 'status')
    list_filter = ('expire_at', 'status')