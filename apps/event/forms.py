from django import forms
from apps.core.models import Guest


class RSVPForm(forms.ModelForm):
    class Meta:
        model = Guest
        fields = ['full_name', 'email', 'phone', 'group', 'meal_choice', 'plus_one', 'plus_one_name', 'notes']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'block w-full px-0 py-3 text-on-surface bg-transparent border-0 border-b-2 border-outline-variant appearance-none focus:outline-none focus:ring-0 focus:border-secondary peer font-body-md text-body-md',
                'placeholder': ' '
            }),
            'email': forms.EmailInput(attrs={
                'class': 'block w-full px-0 py-3 text-on-surface bg-transparent border-0 border-b-2 border-outline-variant appearance-none focus:outline-none focus:ring-0 focus:border-secondary peer font-body-md text-body-md',
                'placeholder': ' '
            }),
            'phone': forms.TextInput(attrs={
                'class': 'block w-full px-0 py-3 text-on-surface bg-transparent border-0 border-b-2 border-outline-variant appearance-none focus:outline-none focus:ring-0 focus:border-secondary peer font-body-md text-body-md',
                'placeholder': ' '
            }),
            'group': forms.Select(attrs={
                'class': 'block w-full px-4 py-3 text-on-surface bg-surface-bright border border-outline-variant rounded appearance-none focus:outline-none focus:ring-1 focus:ring-secondary focus:border-secondary font-body-md text-body-md cursor-pointer'
            }),
            'meal_choice': forms.Select(attrs={
                'class': 'block w-full px-4 py-3 text-on-surface bg-surface-bright border border-outline-variant rounded appearance-none focus:outline-none focus:ring-1 focus:ring-secondary focus:border-secondary font-body-md text-body-md cursor-pointer'
            }),
            'plus_one': forms.CheckboxInput(attrs={
                'class': 'form-checkbox text-secondary focus:ring-secondary border-outline-variant rounded'
            }),
            'plus_one_name': forms.TextInput(attrs={
                'class': 'block w-full px-0 py-3 text-on-surface bg-transparent border-0 border-b-2 border-outline-variant appearance-none focus:outline-none focus:ring-0 focus:border-secondary peer font-body-md text-body-md',
                'placeholder': ' '
            }),
            'notes': forms.Textarea(attrs={
                'class': 'block w-full px-0 py-3 text-on-surface bg-transparent border-0 border-b-2 border-outline-variant appearance-none focus:outline-none focus:ring-0 focus:border-secondary peer font-body-md text-body-md resize-none',
                'placeholder': ' ',
                'rows': '2'
            }),
        }
