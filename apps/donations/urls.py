from django.urls import path
from .views import (
    DonationView, CreatePreferenceView, webhook,
    DonationSuccessView, DonationFailureView, DonationPendingView
)

app_name = 'donations'

urlpatterns = [
    path('', DonationView.as_view(), name='donation'),
    path('preference/', CreatePreferenceView.as_view(), name='preference'),
    path('webhook/', webhook, name='webhook'),
    path('success/', DonationSuccessView.as_view(), name='success'),
    path('failure/', DonationFailureView.as_view(), name='failure'),
    path('pending/', DonationPendingView.as_view(), name='pending'),
]
