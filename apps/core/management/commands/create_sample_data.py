from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.core.models import Event, Guest, Table, ChecklistItem, BudgetItem, CustomUser
from decimal import Decimal
from datetime import date, timedelta


class Command(BaseCommand):
    help = 'Creates sample data for testing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Delete existing sample data before creating new data',
        )

    def handle(self, *args, **options):
        if options['reset']:
            self.stdout.write('Resetting sample data...')
            Event.objects.filter(slug='sarah-james-wedding').delete()
            self.stdout.write('Deleted existing sample data.')

        self.stdout.write('Creating sample data...')
        
        event, created = Event.objects.get_or_create(
            slug='sarah-james-wedding',
            defaults={
                'name': 'Sarah & James',
                'bride_name': 'Sarah',
                'groom_name': 'James',
                'date': date.today() + timedelta(days=142),
                'location': 'Villa Ethereal, Toscana, Italia',
                'venue_details': 'Jardines de la Villa - Vía Delle Vigne 42',
                'budget_total': Decimal('25000.00'),
            }
        )
        
        if created:
            self.stdout.write(f'Created event: {event.name}')
        else:
            self.stdout.write(f'Event already exists: {event.name}')

        user = CustomUser.objects.filter(username='admin').first()
        if user:
            user.event = event
            user.save()
            self.stdout.write(f'Updated admin user with event')

        guests_data = [
            ('Eleanor Vance', 'eleanor@example.com', 'NOVIA', 'PENDING'),
            ('Theodora Crain', 'theodora@example.com', 'NOVIO', 'CONFIRMED'),
            ('Luke Sanderson', 'luke@example.com', 'AMIGOS_NOVIA', 'CONFIRMED'),
            ('Victoria Hart', 'victoria@example.com', 'NOVIA', 'CONFIRMED'),
            ('James Whitmore', 'james.w@example.com', 'NOVIO', 'PENDING'),
            ('Sophia Bennett', 'sophia@example.com', 'AMIGOS_NOVIA', 'CONFIRMED'),
            ('William Chen', 'william@example.com', 'TRABAJO', 'PENDING'),
            ('Isabella Torres', 'isabella@example.com', 'AMIGOS_NOVIO', 'CONFIRMED'),
        ]
        
        for name, email, group, rsvp in guests_data:
            guest, created = Guest.objects.get_or_create(
                email=email,
                defaults={
                    'event': event,
                    'full_name': name,
                    'group': group,
                    'rsvp_status': rsvp,
                    'meal_choice': 'STANDARD',
                }
            )
            if created:
                self.stdout.write(f'Created guest: {name}')

        tables_data = [
            ('Mesa 1', 8, 'CIRCULAR', 25, 20, False),
            ('Mesa 2', 10, 'RECTANGULAR', 60, 50, False),
            ('Mesa 3', 8, 'CIRCULAR', 60, 20, False),
            ('Mesa Principal', 2, 'RECTANGULAR', 50, 10, True),
        ]
        
        for name, capacity, shape, x, y, is_head in tables_data:
            table, created = Table.objects.get_or_create(
                event=event,
                name=name,
                defaults={
                    'capacity': capacity,
                    'shape': shape,
                    'position_x': x,
                    'position_y': y,
                    'is_head_table': is_head,
                }
            )
            if created:
                self.stdout.write(f'Created table: {name}')

        checklist_data = [
            ('Reservar lugar', True, 'HIGH', None),
            ('Contratar fotógrafo', True, 'HIGH', None),
            ('Enviar invitaciones', False, 'HIGH', date.today() + timedelta(days=30)),
            ('Finalizar menú', False, 'MEDIUM', date.today() + timedelta(days=60)),
            ('Seleccionar flores', False, 'MEDIUM', date.today() + timedelta(days=45)),
            ('Planificar música', False, 'LOW', date.today() + timedelta(days=90)),
            ('Ordenar vestido', True, 'HIGH', None),
        ]
        
        for title, completed, priority, due_date in checklist_data:
            item, created = ChecklistItem.objects.get_or_create(
                event=event,
                title=title,
                defaults={
                    'is_completed': completed,
                    'priority': priority,
                    'due_date': due_date,
                }
            )
            if created:
                self.stdout.write(f'Created checklist item: {title}')

        budget_data = [
            ('VENUE', 'Lugar y jardines', Decimal('8000.00'), Decimal('8000.00')),
            ('CATERING', 'Catering y bebidas', Decimal('6000.00'), Decimal('5200.00')),
            ('ATTIRE', 'Vestuario nupcial', Decimal('3500.00'), Decimal('3150.00')),
            ('PHOTOGRAPHY', 'Fotógrafo y videógrafo', Decimal('2500.00'), Decimal('2200.00')),
            ('FLOWERS', 'Arreglos florales', Decimal('1500.00'), Decimal('1200.00')),
            ('MUSIC', 'Banda y DJ', Decimal('1500.00'), Decimal('1000.00')),
        ]
        
        for category, desc, estimated, actual in budget_data:
            item, created = BudgetItem.objects.get_or_create(
                event=event,
                category=category,
                defaults={
                    'description': desc,
                    'estimated_cost': estimated,
                    'actual_cost': actual,
                }
            )
            if created:
                self.stdout.write(f'Created budget item: {desc}')

        self.stdout.write(self.style.SUCCESS('Sample data created successfully!'))
