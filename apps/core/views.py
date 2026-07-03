from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, CreateView
from django.urls import reverse_lazy, reverse
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django import forms
from .models import Event

User = get_user_model()


class CustomLoginView(LoginView):
    template_name = 'core/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        if self.request.user.role == 'GUEST':
            return reverse('gallery:home')
        return reverse('dashboard:home')


class CustomLogoutView(LogoutView):
    next_page = 'event:public'
    http_method_names = ['get', 'post']
    
    def get(self, request, *args, **kwargs):
        from django.contrib.auth import logout
        logout(request)
        return redirect(self.get_next_page())
    
    def get_next_page(self):
        return reverse('event:public')


class SignUpForm(forms.ModelForm):
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'}))
    password2 = forms.CharField(label='Confirmar Contraseña', widget=forms.PasswordInput(attrs={'placeholder': 'Confirmar contraseña'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'role']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Usuario'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Correo electrónico'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Nombre'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Apellido'}),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Las contraseñas no coinciden')
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.role = 'PLANNER'
        event = Event.objects.first()
        if event:
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
