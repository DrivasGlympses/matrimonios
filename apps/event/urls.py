from django.urls import path
from .views import (
    LandingView, GuestHomeView,
    InvitationView, ConfirmInvitationView,
    InvitationConfirmedView, InvitationDeclinedView,
    InvitationExpiredView
)

app_name = 'event'

urlpatterns = [
    path('landing/', LandingView.as_view(), name='landing'),
    path('guest/', GuestHomeView.as_view(), name='guest_home'),
    path('invitacion/<uuid:token>/', InvitationView.as_view(), name='invitation'),
    path('invitacion/<uuid:token>/confirmar/', ConfirmInvitationView.as_view(), name='confirm_invitation'),
    path('invitacion/confirmada/', InvitationConfirmedView.as_view(), name='invitation_confirmed'),
    path('invitacion/rechazada/', InvitationDeclinedView.as_view(), name='invitation_declined'),
    path('invitacion/caducada/', InvitationExpiredView.as_view(), name='invitation_expired'),
]
