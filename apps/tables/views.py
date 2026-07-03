import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from apps.core.models import Event, Guest, Table
from apps.core.views import PlannerRequiredMixin


def get_user_event(user):
    if user.is_authenticated and hasattr(user, 'event') and user.event:
        return user.event
    return Event.objects.first()


class TablesHomeView(PlannerRequiredMixin, ListView):
    template_name = 'tables/tables.html'
    model = Table
    context_object_name = 'tables'
    
    def get_queryset(self):
        event = get_user_event(self.request.user)
        if event:
            return event.tables.all()
        return Table.objects.none()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = get_user_event(self.request.user)
        context['event'] = event
        context['confirmed_guests'] = event.guests.filter(rsvp_status='CONFIRMED', linked_to__isnull=True).count() if event else 0
        context['pending_guests'] = event.guests.filter(rsvp_status='PENDING', linked_to__isnull=True).count() if event else 0
        if event:
            context['unassigned_guests'] = list(event.guests.filter(assigned_table__isnull=True, rsvp_status='CONFIRMED', linked_to__isnull=True))
            context['all_guests'] = list(event.guests.filter(rsvp_status='CONFIRMED', linked_to__isnull=True))
            tables_data = []
            for t in event.tables.all():
                guests_with_plus_ones = []
                for g in t.get_main_guests():
                    guests_with_plus_ones.append({
                        'id': g.id,
                        'name': g.full_name,
                        'group': g.group,
                        'is_plus_one': False,
                    })
                    po = g.get_plus_one()
                    if po:
                        guests_with_plus_ones.append({
                            'id': po.id,
                            'name': po.full_name,
                            'group': po.group,
                            'is_plus_one': True,
                            'plus_one_of': g.full_name,
                        })
                tables_data.append({
                    'id': t.id,
                    'name': t.name,
                    'capacity': t.capacity,
                    'shape': t.shape,
                    'position_x': t.position_x,
                    'position_y': t.position_y,
                    'is_head_table': t.is_head_table,
                    'guests_count': t.assigned_guests_count,
                    'guests': guests_with_plus_ones,
                })
            context['tables_json'] = json.dumps(tables_data)
            context['unassigned_json'] = json.dumps([
                {'id': g.id, 'name': g.full_name, 'group': g.group}
                for g in event.guests.filter(assigned_table__isnull=True, rsvp_status='CONFIRMED', linked_to__isnull=True)
            ])
        else:
            context['unassigned_guests'] = []
            context['all_guests'] = []
            context['tables_json'] = '[]'
            context['unassigned_json'] = '[]'
        return context


class TableCreateView(PlannerRequiredMixin, CreateView):
    model = Table
    fields = ['name', 'capacity', 'shape', 'position_x', 'position_y', 'is_head_table']
    template_name = 'tables/table_form.html'
    success_url = reverse_lazy('tables:home')
    
    def get(self, request, *args, **kwargs):
        event = get_user_event(request.user)
        if not event:
            return redirect('dashboard:event_settings')
        return super().get(request, *args, **kwargs)
    
    def form_valid(self, form):
        event = get_user_event(self.request.user)
        if event:
            form.instance.event = event
        return super().form_valid(form)


class TableUpdateView(PlannerRequiredMixin, UpdateView):
    model = Table
    fields = ['name', 'capacity', 'shape', 'position_x', 'position_y', 'is_head_table']
    success_url = reverse_lazy('tables:home')
    template_name = 'tables/table_form.html'


class TableDeleteView(PlannerRequiredMixin, DeleteView):
    model = Table
    template_name = 'tables/table_confirm_delete.html'
    success_url = reverse_lazy('tables:home')


@csrf_exempt
@login_required
@require_http_methods(["POST"])
def assign_guest_to_table(request, guest_id, table_id):
    if request.user.role != 'PLANNER':
        return JsonResponse({'error': 'No autorizado'}, status=403)
    
    guest = get_object_or_404(Guest, pk=guest_id)
    
    if table_id:
        table = get_object_or_404(Table, pk=table_id)
        guest.assigned_table = table
        guest.save()
        
        if guest.plus_one and guest.plus_one_name:
            plus_one = guest.plus_ones.first()
            
            if not plus_one:
                plus_one = Guest.objects.create(
                    event=guest.event,
                    full_name=guest.plus_one_name,
                    email='',
                    phone='',
                    group=guest.group,
                    rsvp_status='CONFIRMED',
                    meal_choice=guest.meal_choice,
                    plus_one_name=guest.full_name,
                    linked_to=guest,
                    assigned_table=table,
                )
            else:
                plus_one.assigned_table = table
                plus_one.group = guest.group
                plus_one.meal_choice = guest.meal_choice
                plus_one.save()
    else:
        guest.assigned_table = None
        guest.save()
        
        guest.plus_ones.update(assigned_table=None)
    
    return JsonResponse({
        'success': True,
        'guest_id': guest_id,
        'table_id': table_id,
        'guest_name': guest.full_name
    })


@csrf_exempt
@login_required
@require_http_methods(["POST"])
def update_table_position(request, table_id):
    if request.user.role != 'PLANNER':
        return JsonResponse({'error': 'No autorizado'}, status=403)
    
    table = get_object_or_404(Table, pk=table_id)
    x = request.POST.get('x', 0)
    y = request.POST.get('y', 0)
    table.position_x = float(x)
    table.position_y = float(y)
    table.save()
    
    return JsonResponse({'success': True, 'x': x, 'y': y})


def get_guests_by_table(request, table_id):
    table = get_object_or_404(Table, pk=table_id)
    guests_data = []
    
    for g in table.get_main_guests():
        guests_data.append({
            'id': g.id,
            'name': g.full_name,
            'initials': ''.join([n[0] for n in g.full_name.split()[:2]]).upper(),
            'is_plus_one': False,
        })
        po = g.get_plus_one()
        if po:
            guests_data.append({
                'id': po.id,
                'name': po.full_name,
                'initials': ''.join([n[0] for n in po.full_name.split()[:2]]).upper(),
                'is_plus_one': True,
                'plus_one_of': g.full_name,
            })
    
    return JsonResponse({'guests': guests_data})


@csrf_exempt
@login_required
@require_http_methods(["GET"])
def get_guest_details(request, guest_id):
    if request.user.role != 'PLANNER':
        return JsonResponse({'error': 'No autorizado'}, status=403)
    
    guest = get_object_or_404(Guest, pk=guest_id)
    
    return JsonResponse({
        'id': guest.id,
        'full_name': guest.full_name,
        'email': guest.email,
        'phone': guest.phone,
        'group': guest.group,
        'group_display': guest.get_group_display(),
        'rsvp_status': guest.rsvp_status,
        'rsvp_display': guest.get_rsvp_status_display(),
        'meal_choice': guest.meal_choice,
        'meal_display': guest.get_meal_choice_display(),
        'plus_one': guest.plus_one,
        'plus_one_name': guest.plus_one_name,
        'notes': guest.notes,
        'assigned_table': guest.assigned_table.id if guest.assigned_table else None,
        'assigned_table_name': guest.assigned_table.name if guest.assigned_table else None,
    })


@csrf_exempt
@login_required
@require_http_methods(["POST"])
def update_guest_details(request, guest_id):
    if request.user.role != 'PLANNER':
        return JsonResponse({'error': 'No autorizado'}, status=403)
    
    guest = get_object_or_404(Guest, pk=guest_id)
    
    data = request.POST
    if 'full_name' in data:
        guest.full_name = data['full_name']
    if 'email' in data:
        guest.email = data['email']
    if 'phone' in data:
        guest.phone = data['phone']
    if 'group' in data:
        guest.group = data['group']
    if 'rsvp_status' in data:
        guest.rsvp_status = data['rsvp_status']
    if 'meal_choice' in data:
        guest.meal_choice = data['meal_choice']
    if 'notes' in data:
        guest.notes = data['notes']
    
    old_plus_one = guest.plus_one
    old_plus_one_name = guest.plus_one_name
    
    if 'plus_one' in data:
        guest.plus_one = data['plus_one'] == 'true'
    if 'plus_one_name' in data:
        guest.plus_one_name = data['plus_one_name']
    
    guest.save()
    
    existing_plus_one = guest.plus_ones.first()
    
    if guest.plus_one and guest.plus_one_name:
        if existing_plus_one:
            existing_plus_one.full_name = guest.plus_one_name
            existing_plus_one.group = guest.group
            existing_plus_one.meal_choice = guest.meal_choice
            existing_plus_one.save()
        else:
            Guest.objects.create(
                event=guest.event,
                full_name=guest.plus_one_name,
                email='',
                phone='',
                group=guest.group,
                rsvp_status='CONFIRMED',
                meal_choice=guest.meal_choice,
                plus_one_name=guest.full_name,
                linked_to=guest,
                assigned_table=guest.assigned_table,
            )
    else:
        if existing_plus_one:
            existing_plus_one.delete()
        guest.plus_one_name = ''
        guest.plus_one = False
        guest.save()
    
    return JsonResponse({'success': True, 'guest_name': guest.full_name})
