from django.urls import path
from .views import (
    DashboardHomeView, ChecklistView, toggle_checklist_item, EventSettingsView,
    GuestListView, GuestCreateView, GuestUpdateView, GuestDeleteView,
    import_guests, export_guests, download_guest_template,
    ChecklistItemCreateView, ChecklistItemUpdateView, ChecklistItemDeleteView,
    BudgetView, BudgetItemCreateView, BudgetItemUpdateView, BudgetItemDeleteView,
    email_preview
)

app_name = 'dashboard'

urlpatterns = [
    path('', DashboardHomeView.as_view(), name='home'),
    path('event/', EventSettingsView.as_view(), name='event_settings'),
    path('event/email-preview/', email_preview, name='email_preview'),
    path('guests/', GuestListView.as_view(), name='guests'),
    path('guests/add/', GuestCreateView.as_view(), name='guest_add'),
    path('guests/<int:pk>/edit/', GuestUpdateView.as_view(), name='guest_edit'),
    path('guests/<int:pk>/delete/', GuestDeleteView.as_view(), name='guest_delete'),
    path('guests/import/', import_guests, name='guests_import'),
    path('guests/export/', export_guests, name='guests_export'),
    path('guests/template/', download_guest_template, name='guests_template'),
    path('checklist/', ChecklistView.as_view(), name='checklist'),
    path('checklist/add/', ChecklistItemCreateView.as_view(), name='checklist_add'),
    path('checklist/<int:pk>/edit/', ChecklistItemUpdateView.as_view(), name='checklist_edit'),
    path('checklist/<int:pk>/delete/', ChecklistItemDeleteView.as_view(), name='checklist_delete'),
    path('checklist/toggle/<int:pk>/', toggle_checklist_item, name='toggle_checklist'),
    path('budget/', BudgetView.as_view(), name='budget'),
    path('budget/add/', BudgetItemCreateView.as_view(), name='budget_add'),
    path('budget/<int:pk>/edit/', BudgetItemUpdateView.as_view(), name='budget_edit'),
    path('budget/<int:pk>/delete/', BudgetItemDeleteView.as_view(), name='budget_delete'),
]
