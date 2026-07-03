from django.db import models
from apps.core.models import Guest


class Donation(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pendiente'),
        ('APPROVED', 'Aprobada'),
        ('REJECTED', 'Rechazada'),
    ]
    
    CURRENCY_CHOICES = [
        ('CLP', 'Peso Chileno'),
        ('USD', 'Dólar Estadounidense'),
    ]
    
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE, related_name='donations')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='CLP')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    mercadopago_payment_id = models.CharField(max_length=255, blank=True)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Donación'
        verbose_name_plural = 'Donaciones'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.guest.full_name} - {self.amount} {self.currency}"
