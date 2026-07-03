from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Event, Guest, Table, Photo, ChecklistItem, BudgetItem


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'role', 'event', 'is_staff']
    list_filter = ['role', 'is_staff', 'is_active']
    fieldsets = UserAdmin.fieldsets + (
        ('Información adicional', {'fields': ('role', 'phone', 'event')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información adicional', {'fields': ('role', 'phone', 'event')}),
    )


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'bride_name', 'groom_name', 'date', 'location', 'budget_total', 'total_guests', 'confirmed_guests']
    search_fields = ['name', 'bride_name', 'groom_name', 'location']
    fieldsets = (
        (None, {
            'fields': ('bride_name', 'groom_name', 'name', 'slug')
        }),
        ('Detalles del Evento', {
            'fields': ('date', 'location', 'venue_details', 'couple_photo', 'budget_total')
        }),
    )


@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'group', 'rsvp_status', 'meal_choice', 'assigned_table', 'event']
    list_filter = ['rsvp_status', 'meal_choice', 'group', 'event']
    search_fields = ['full_name', 'email']
    raw_id_fields = ['assigned_table', 'user']


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ['name', 'event', 'capacity', 'shape', 'assigned_guests_count', 'is_head_table']
    list_filter = ['shape', 'is_head_table', 'event']


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ['event', 'uploaded_by', 'category', 'caption', 'created_at']
    list_filter = ['category', 'event']
    search_fields = ['caption']


@admin.register(ChecklistItem)
class ChecklistItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'event', 'is_completed', 'priority', 'due_date']
    list_filter = ['is_completed', 'priority', 'event']


@admin.register(BudgetItem)
class BudgetItemAdmin(admin.ModelAdmin):
    list_display = ['description', 'category', 'estimated_cost', 'actual_cost', 'difference', 'event']
    list_filter = ['category', 'event']
