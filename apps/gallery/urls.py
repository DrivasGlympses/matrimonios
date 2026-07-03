from django.urls import path
from .views import GalleryHomeView, PhotoUploadView, PhotoDeleteView, get_photos_by_category

app_name = 'gallery'

urlpatterns = [
    path('', GalleryHomeView.as_view(), name='home'),
    path('upload/', PhotoUploadView.as_view(), name='upload'),
    path('delete/<int:pk>/', PhotoDeleteView.as_view(), name='delete'),
    path('api/category/<str:category>/', get_photos_by_category, name='by_category'),
]
