from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.event.views import LandingView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('apps.core.urls')),
    path('dashboard/', include('apps.dashboard.urls')),
    path('tables/', include('apps.tables.urls')),
    path('gallery/', include('apps.gallery.urls')),
    path('donations/', include('apps.donations.urls')),
    path('', LandingView.as_view(), name='landing'),
    path('', include('apps.event.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
