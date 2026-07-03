from django.urls import path
from .views import (
    PublicEventView, RSVPView, RSVPSuccessView,
    InvitationView, ConfirmInvitationView,
    InvitationConfirmedView, InvitationDeclinedView,
    InvitationExpiredView
)

app_name = 'event'

urlpatterns = [
    path('', PublicEventView.as_view(), name='public'),
    path('rsvp/', RSVPView.as_view(), name='rsvp'),
    path('rsvp/gracias/', RSVPSuccessView.as_view(), name='rsvp_success'),
    path('invitacion/<uuid:token>/', InvitationView.as_view(), name='invitation'),
    path('invitacion/<uuid:token>/confirmar/', ConfirmInvitationView.as_view(), name='confirm_invitation'),
    path('invitacion/confirmada/', InvitationConfirmedView.as_view(), name='invitation_confirmed'),
    path('invitacion/rechazada/', InvitationDeclinedView.as_view(), name='invitation_declined'),
    path('invitacion/caducada/', InvitationExpiredView.as_view(), name='invitation_expired'),
]
