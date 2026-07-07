from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetConfirmView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, CreateView
from django.urls import reverse_lazy, reverse
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django import forms
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.conf import settings
from .models import Event

User = get_user_model()


class CustomLoginView(LoginView):
    template_name = 'core/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        if self.request.user.role == 'GUEST':
            return reverse('event:guest_home')
        return reverse('dashboard:home')


class CustomLogoutView(LogoutView):
    next_page = 'landing'
    http_method_names = ['get', 'post']
    
    def get(self, request, *args, **kwargs):
        from django.contrib.auth import logout
        logout(request)
        return redirect(self.get_next_page())
    
    def get_next_page(self):
        return reverse('landing')


class CustomPasswordResetView(PasswordResetView):
    template_name = 'core/password_reset.html'
    email_template_name = 'core/password_reset_email.html'
    subject_template_name = 'core/password_reset_subject.txt'
    success_url = '/accounts/password-reset/done/'
    html_email_template_name = 'core/password_reset_email.html'

    def send_mail(self, subject_template_name, email_template_name, context, from_email, to_email, html_email_template_name=None):
        subject = render_to_string(subject_template_name, context).strip()
        html_body = render_to_string(html_email_template_name or email_template_name, context)
        from apps.core.emails import send_mailgun_email
        send_mailgun_email(
            to_email=to_email,
            subject=subject,
            html_content=html_body,
            from_email=from_email,
        )


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'core/password_reset_confirm.html'
    success_url = '/accounts/password-reset-complete/'


class SignUpForm(forms.ModelForm):
    password1 = forms.CharField(label='Contrasena', widget=forms.PasswordInput(attrs={'placeholder': 'Contrasena'}))
    password2 = forms.CharField(label='Confirmar Contrasena', widget=forms.PasswordInput(attrs={'placeholder': 'Confirmar contrasena'}))
    bride_name = forms.CharField(label='Nombre de la Novia', widget=forms.TextInput(attrs={'placeholder': 'Nombre de la novia'}), required=False)
    groom_name = forms.CharField(label='Nombre del Novio', widget=forms.TextInput(attrs={'placeholder': 'Nombre del novio'}), required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'role']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Usuario'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Correo electronico'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Nombre'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Apellido'}),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Las contrasenas no coinciden')
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.role = 'PLANNER'
        bride = self.cleaned_data.get('bride_name', '')
        groom = self.cleaned_data.get('groom_name', '')
        event = Event.objects.create(
            bride_name=bride,
            groom_name=groom,
        )
        user.event = event
        if commit:
            user.save()
        return user


class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'core/signup.html'
    success_url = reverse_lazy('dashboard:home')


class PlannerRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if request.user.role != 'PLANNER':
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
