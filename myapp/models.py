from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cpf = models.CharField(max_length=11)
    birth_date = models.DateField()
    phone_number = models.CharField(max_length=20)
    
    def __str__(self):
        return self.user.username

class Charge(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Charge for {self.customer.user.username} - {self.value}"

class Boleto(models.Model):
    charge = models.OneToOneField(Charge, on_delete=models.CASCADE)
    expire_at = models.DateField()
    barcode = models.CharField(max_length=100)
    pdf = models.URLField()
    status = models.CharField(max_length=20)
    qrcode = models.TextField(null=True, blank=True)  # Adicionando campo para QR code
    pix_key = models.TextField(null=True, blank=True)  # Adicionando campo para chave Pix
    
    
    def __str__(self):
        return f"Boleto for {self.charge.customer.user.username}"