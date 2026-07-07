from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.conf import settings
import requests
import json
import logging
from .models import Donation

logger = logging.getLogger(__name__)


class DonationView(LoginRequiredMixin, TemplateView):
    def get_template_names(self):
        if self.request.user.role == 'GUEST':
            return ['donations/guest_donation.html']
        return ['donations/donation.html']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if hasattr(self.request.user, 'guest_profile'):
            context['guest'] = self.request.user.guest_profile
            context['event'] = self.request.user.event
            context['public_key'] = settings.MERCADOPAGO_PUBLIC_KEY
        return context


class CreatePreferenceView(LoginRequiredMixin, View):
    def post(self, request):
        if not hasattr(request.user, 'guest_profile'):
            return JsonResponse({'error': 'No autorizado'}, status=403)
        
        guest = request.user.guest_profile
        amount = request.POST.get('amount')
        message = request.POST.get('message', '')
        
        try:
            amount = float(amount)
            if amount <= 0:
                return JsonResponse({'error': 'Monto inválido'}, status=400)
        except (ValueError, TypeError):
            return JsonResponse({'error': 'Monto inválido'}, status=400)
        
        donation = Donation.objects.create(
            guest=guest,
            amount=amount,
            currency='CLP',
            message=message,
            status='PENDING'
        )
        
        try:
            base_url = request.build_absolute_uri('/').rstrip('/')
            
            base_url = settings.SITE_URL.rstrip('/')
            
            preference_data = {
                'items': [
                    {
                        'id': str(donation.id),
                        'title': f'Donación para {guest.event.display_name}',
                        'quantity': 1,
                        'unit_price': float(amount),
                        'currency_id': 'CLP',
                    }
                ],
                'back_urls': {
                    'success': f'{base_url}/donations/success/',
                    'failure': f'{base_url}/donations/failure/',
                    'pending': f'{base_url}/donations/pending/',
                },
                'auto_return': 'approved',
                'notification_url': f'{base_url}/donations/webhook/',
                'external_reference': str(donation.id),
            }
            
            logger.info('Payload enviado a Mercado Pago: %s', json.dumps(preference_data, indent=2))
            
            headers = {
                'Authorization': f'Bearer {settings.MERCADOPAGO_ACCESS_TOKEN}',
                'Content-Type': 'application/json',
            }
            
            logger.info('Sending to Mercado Pago: %s', preference_data)
            logger.info('Headers: %s', {k: v[:20] + '...' if k == 'Authorization' else v for k, v in headers.items()})
            
            response = requests.post(
                'https://api.mercadopago.com/checkout/preferences',
                json=preference_data,
                headers=headers
            )
            
            logger.info('Mercado Pago response status: %s', response.status_code)
            logger.info('Mercado Pago response body: %s', response.text)
            
            if response.status_code in [200, 201]:
                data = response.json()
                return JsonResponse({
                    'preference_id': data['id'],
                    'init_point': data.get('init_point', data.get('sandbox_init_point')),
                })
            else:
                error_data = response.json()
                logger.error('Mercado Pago error: %s', error_data)
                return JsonResponse({
                    'error': error_data.get('message', 'Error de Mercado Pago'),
                    'details': error_data
                }, status=response.status_code)
            
        except Exception as e:
            donation.delete()
            logger.exception('Error creating preference')
            return JsonResponse({'error': f'Error al crear preferencia: {str(e)}'}, status=500)


@csrf_exempt
@require_POST
def webhook(request):
    try:
        import json
        data = json.loads(request.body)
        
        if data.get('type') == 'payment':
            payment_id = data.get('data', {}).get('id')
            
            headers = {
                'Authorization': f'Bearer {settings.MERCADOPAGO_ACCESS_TOKEN}',
            }
            
            response = requests.get(
                f'https://api.mercadopago.com/v1/payments/{payment_id}',
                headers=headers
            )
            
            if response.status_code == 200:
                payment = response.json()
                donation_id = payment.get('external_reference')
                if donation_id:
                    donation = Donation.objects.get(id=donation_id)
                    
                    if payment['status'] == 'approved':
                        donation.status = 'APPROVED'
                        donation.mercadopago_payment_id = payment_id
                        donation.save()
                    elif payment['status'] in ['rejected', 'cancelled']:
                        donation.status = 'REJECTED'
                        donation.save()
        
        return JsonResponse({'status': 'ok'})
        
    except Exception as e:
        logger.exception('Webhook error')
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


class DonationSuccessView(LoginRequiredMixin, TemplateView):
    def get_template_names(self):
        if self.request.user.role == 'GUEST':
            return ['donations/guest_success.html']
        return ['donations/success.html']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if hasattr(self.request.user, 'guest_profile'):
            context['event'] = self.request.user.event
        elif self.request.user.role == 'PLANNER' and self.request.user.event:
            context['event'] = self.request.user.event
        return context


class DonationFailureView(LoginRequiredMixin, TemplateView):
    def get_template_names(self):
        if self.request.user.role == 'GUEST':
            return ['donations/guest_failure.html']
        return ['donations/failure.html']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if hasattr(self.request.user, 'guest_profile'):
            context['event'] = self.request.user.event
        elif self.request.user.role == 'PLANNER' and self.request.user.event:
            context['event'] = self.request.user.event
        return context


class DonationPendingView(LoginRequiredMixin, TemplateView):
    def get_template_names(self):
        if self.request.user.role == 'GUEST':
            return ['donations/guest_pending.html']
        return ['donations/pending.html']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if hasattr(self.request.user, 'guest_profile'):
            context['event'] = self.request.user.event
        elif self.request.user.role == 'PLANNER' and self.request.user.event:
            context['event'] = self.request.user.event
        return context
