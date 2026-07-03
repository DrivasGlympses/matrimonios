from django.urls import path
from .views import (
    TablesHomeView, TableCreateView, TableUpdateView, TableDeleteView,
    assign_guest_to_table, update_table_position, get_guests_by_table,
    get_guest_details, update_guest_details
)

app_name = 'tables'

urlpatterns = [
    path('', TablesHomeView.as_view(), name='home'),
    path('create/', TableCreateView.as_view(), name='create'),
    path('update/<int:pk>/', TableUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', TableDeleteView.as_view(), name='delete'),
    path('api/assign/<int:guest_id>/<int:table_id>/', assign_guest_to_table, name='assign_guest'),
    path('api/position/<int:table_id>/', update_table_position, name='update_position'),
    path('api/guests/<int:table_id>/', get_guests_by_table, name='get_guests'),
    path('api/guest/<int:guest_id>/', get_guest_details, name='get_guest_details'),
    path('api/guest/<int:guest_id>/update/', update_guest_details, name='update_guest_details'),
]
