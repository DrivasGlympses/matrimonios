from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import JsonResponse
from apps.core.models import Event, Photo
from apps.core.views import PlannerRequiredMixin


class GalleryHomeView(LoginRequiredMixin, ListView):
    model = Photo
    context_object_name = 'photos'
    
    def get_template_names(self):
        if self.request.user.role == 'GUEST':
            return ['gallery/guest_gallery.html']
        return ['gallery/gallery.html']
    
    def get_queryset(self):
        event = Event.objects.first()
        if event:
            return event.photos.all()
        return Photo.objects.none()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event'] = Event.objects.first()
        context['categories'] = Photo.CATEGORY_CHOICES
        return context


class PhotoUploadView(PlannerRequiredMixin, CreateView):
    model = Photo
    fields = ['image', 'category', 'caption']
    success_url = reverse_lazy('gallery:home')
    template_name = 'gallery/upload.html'
    
    def form_valid(self, form):
        event = Event.objects.first()
        if event:
            form.instance.event = event
            form.instance.uploaded_by = self.request.user
        return super().form_valid(form)


class PhotoDeleteView(PlannerRequiredMixin, DeleteView):
    model = Photo
    success_url = reverse_lazy('gallery:home')
    
    def get_queryset(self):
        return Photo.objects.filter(uploaded_by=self.request.user)


def get_photos_by_category(request, category):
    event = Event.objects.first()
    if event:
        photos = event.photos.filter(category=category)
    else:
        photos = Photo.objects.none()
    
    return JsonResponse({
        'photos': [
            {
                'id': p.id,
                'url': p.image.url,
                'caption': p.caption,
                'author': p.uploaded_by.get_full_name() or p.uploaded_by.username,
                'category': p.get_category_display()
            }
            for p in photos
        ]
    })
