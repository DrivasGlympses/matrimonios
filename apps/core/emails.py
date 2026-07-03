import requests
from django.template.loader import render_to_string
from django.conf import settings
from django.urls import reverse


def send_mailgun_email(to_email, subject, html_content, from_email=None):
    if not settings.MAILGUN_API_KEY or not settings.MAILGUN_DOMAIN:
        raise ValueError('MAILGUN_API_KEY y MAILGUN_DOMAIN deben estar configurados')
    
    from_email = from_email or settings.MAILGUN_FROM_EMAIL
    api_url = f'https://api.mailgun.net/v3/{settings.MAILGUN_DOMAIN}/messages'
    
    response = requests.post(
        api_url,
        auth=('api', settings.MAILGUN_API_KEY),
        data={
            'from': from_email,
            'to': [to_email],
            'subject': subject,
            'html': html_content,
        },
        timeout=30,
    )
    
    response.raise_for_status()
    return response.json()


def send_invitation_email(guest):
    invitation_url = settings.SITE_URL + reverse('event:invitation', kwargs={'token': guest.invitation_token})
    
    template_map = {
        'classic_romance': 'emails/invitations/classic_romance.html',
        'modern_minimal': 'emails/invitations/modern_minimal.html',
        'rustic_boho': 'emails/invitations/rustic_boho.html',
        'art_deco': 'emails/invitations/art_deco.html',
        'floral_romantic': 'emails/invitations/floral_romantic.html',
    }
    
    design = guest.event.design_template if guest.event else 'classic_romance'
    email_template = template_map.get(design, 'emails/invitations/classic_romance.html')
    
    context = {
        'guest': guest,
        'event': guest.event,
        'invitation_url': invitation_url,
    }
    
    html_message = render_to_string(email_template, context)
    
    send_mailgun_email(
        to_email=guest.email,
        subject=f'Invitación a la boda de {guest.event.display_name}',
        html_content=html_message,
    )
    
    guest.invitation_sent = True
    from django.utils import timezone
    guest.token_created_at = timezone.now()
    guest.save()


def send_credentials_email(guest, password):
    login_url = settings.SITE_URL + reverse('core:login')
    
    template_map = {
        'classic_romance': 'emails/credentials/classic_romance.html',
        'modern_minimal': 'emails/credentials/modern_minimal.html',
        'rustic_boho': 'emails/credentials/rustic_boho.html',
        'art_deco': 'emails/credentials/art_deco.html',
        'floral_romantic': 'emails/credentials/floral_romantic.html',
    }
    
    design = guest.event.design_template if guest.event else 'classic_romance'
    email_template = template_map.get(design, 'emails/credentials/classic_romance.html')
    
    context = {
        'guest': guest,
        'username': guest.user.username,
        'password': password,
        'login_url': login_url,
        'event': guest.event,
    }
    
    html_message = render_to_string(email_template, context)
    
    send_mailgun_email(
        to_email=guest.email,
        subject=f'Tus credenciales para acceder a la galería de {guest.event.display_name}',
        html_content=html_message,
    )
