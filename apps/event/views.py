from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, CreateView, View
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils import timezone
import string
import random
from apps.core.models import Event, Guest
from .forms import RSVPForm


User = get_user_model()


class PublicEventView(TemplateView):
    template_name = 'event/public.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event'] = Event.objects.first()
        return context


class RSVPView(CreateView):
    model = Guest
    form_class = RSVPForm
    template_name = 'event/rsvp_form.html'
    success_url = reverse_lazy('event:rsvp_success')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event'] = Event.objects.first()
        return context
    
    def form_valid(self, form):
        event = Event.objects.first()
        if event:
            form.instance.event = event
            form.instance.rsvp_status = 'CONFIRMED'
        messages.success(self.request, '¡Gracias por confirmar tu asistencia! Te esperamos.')
        return super().form_valid(form)


class RSVPSuccessView(TemplateView):
    template_name = 'event/rsvp_success.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event'] = Event.objects.first()
        return context


class InvitationView(TemplateView):
    
    def get_template_names(self):
        token = self.kwargs.get('token')
        guest = get_object_or_404(Guest, invitation_token=token)
        
        if guest.rsvp_status in ['CONFIRMED', 'DECLINED']:
            template_map = {
                'classic_romance': 'event/expired/classic_romance.html',
                'modern_minimal': 'event/expired/modern_minimal.html',
                'rustic_boho': 'event/expired/rustic_boho.html',
                'art_deco': 'event/expired/art_deco.html',
                'floral_romantic': 'event/expired/floral_romantic.html',
            }
        else:
            template_map = {
                'classic_romance': 'event/invitations/classic_romance.html',
                'modern_minimal': 'event/invitations/modern_minimal.html',
                'rustic_boho': 'event/invitations/rustic_boho.html',
                'art_deco': 'event/invitations/art_deco.html',
                'floral_romantic': 'event/invitations/floral_romantic.html',
            }
        
        design = guest.event.design_template if guest.event else 'classic_romance'
        return [template_map.get(design, template_map.get('classic_romance'))]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        token = kwargs.get('token')
        guest = get_object_or_404(Guest, invitation_token=token)
        context['guest'] = guest
        context['event'] = guest.event
        return context


class ConfirmInvitationView(View):
    def post(self, request, token):
        guest = get_object_or_404(Guest, invitation_token=token)
        
        if guest.rsvp_status in ['CONFIRMED', 'DECLINED']:
            return redirect('event:invitation_expired')
        
        action = request.POST.get('action')
        
        if action == 'accept':
            first_name = guest.full_name.split()[0]
            last_name = guest.full_name.split()[-1] if len(guest.full_name.split()) > 1 else guest.full_name
            
            username = f"{first_name[0].lower()}.{last_name.lower()}"
            
            counter = 1
            base_username = username
            while User.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1
            
            password = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
            
            user = User.objects.create_user(
                username=username,
                email=guest.email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                role='GUEST',
                event=guest.event,
            )
            
            guest.user = user
            guest.rsvp_status = 'CONFIRMED'
            guest.save()
            
            try:
                from apps.core.emails import send_credentials_email
                send_credentials_email(guest, password)
                messages.success(request, '¡Has confirmado tu asistencia! Revisa tu correo para acceder a tus credenciales.')
            except Exception as e:
                messages.warning(request, f'Has confirmado tu asistencia, pero no se pudo enviar el correo con tus credenciales: {str(e)}')
            
            return redirect('event:invitation_confirmed')
        
        elif action == 'decline':
            guest.rsvp_status = 'DECLINED'
            guest.save()
            messages.info(request, 'Lamentamos que no puedas acompañarnos. ¡Gracias por avisarnos!')
            return redirect('event:invitation_declined')
        
        return redirect('event:invitation', token=token)


class InvitationConfirmedView(TemplateView):
    
    def get_template_names(self):
        event = Event.objects.first()
        template_map = {
            'classic_romance': 'event/confirmed/classic_romance.html',
            'modern_minimal': 'event/confirmed/modern_minimal.html',
            'rustic_boho': 'event/confirmed/rustic_boho.html',
            'art_deco': 'event/confirmed/art_deco.html',
            'floral_romantic': 'event/confirmed/floral_romantic.html',
        }
        design = event.design_template if event else 'classic_romance'
        return [template_map.get(design, 'event/confirmed/classic_romance.html')]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event'] = Event.objects.first()
        return context


class InvitationDeclinedView(TemplateView):
    
    def get_template_names(self):
        event = Event.objects.first()
        template_map = {
            'classic_romance': 'event/declined/classic_romance.html',
            'modern_minimal': 'event/declined/modern_minimal.html',
            'rustic_boho': 'event/declined/rustic_boho.html',
            'art_deco': 'event/declined/art_deco.html',
            'floral_romantic': 'event/declined/floral_romantic.html',
        }
        design = event.design_template if event else 'classic_romance'
        return [template_map.get(design, 'event/declined/classic_romance.html')]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event'] = Event.objects.first()
        return context


class InvitationExpiredView(TemplateView):
    
    def get_template_names(self):
        event = Event.objects.first()
        template_map = {
            'classic_romance': 'event/expired/classic_romance.html',
            'modern_minimal': 'event/expired/modern_minimal.html',
            'rustic_boho': 'event/expired/rustic_boho.html',
            'art_deco': 'event/expired/art_deco.html',
            'floral_romantic': 'event/expired/floral_romantic.html',
        }
        design = event.design_template if event else 'classic_romance'
        return [template_map.get(design, 'event/expired/classic_romance.html')]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event'] = Event.objects.first()
        return context
