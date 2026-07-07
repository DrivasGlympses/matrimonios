from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import uuid


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('PLANNER', 'Wedding Planner'),
        ('GUEST', 'Invitado'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='GUEST')
    phone = models.CharField(max_length=20, blank=True)
    event = models.ForeignKey('Event', on_delete=models.CASCADE, null=True, blank=True, related_name='users')
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'


class Event(models.Model):
    DESIGN_TEMPLATE_CHOICES = [
        ('classic_romance', 'Romance Clásico'),
        ('modern_minimal', 'Minimalista Moderno'),
        ('rustic_boho', 'Rústico Boho'),
        ('art_deco', 'Art Deco'),
        ('floral_romantic', 'Floral Romántico'),
    ]
    
    name = models.CharField(max_length=200, blank=True)
    slug = models.SlugField(unique=True, blank=True)
    bride_name = models.CharField(max_length=100, blank=True, verbose_name='Nombre de la Novia')
    groom_name = models.CharField(max_length=100, blank=True, verbose_name='Nombre del Novio')
    date = models.DateField(null=True, blank=True)
    ceremony_time = models.TimeField(null=True, blank=True, verbose_name='Hora de la Ceremonia')
    location = models.CharField(max_length=300, blank=True, verbose_name='Lugar de la Ceremonia')
    venue_details = models.TextField(blank=True, verbose_name='Detalles del Lugar de la Ceremonia')
    latitude = models.FloatField(null=True, blank=True, verbose_name='Latitud de la Ceremonia')
    longitude = models.FloatField(null=True, blank=True, verbose_name='Longitud de la Ceremonia')
    same_venue = models.BooleanField(default=False, verbose_name='Mismo lugar para ceremonia y celebración')
    celebration_time = models.TimeField(null=True, blank=True, verbose_name='Hora de la Celebración')
    celebration_location = models.CharField(max_length=300, blank=True, verbose_name='Lugar de la Celebración')
    celebration_venue_details = models.TextField(blank=True, verbose_name='Detalles del Lugar de la Celebración')
    celebration_latitude = models.FloatField(null=True, blank=True, verbose_name='Latitud de la Celebración')
    celebration_longitude = models.FloatField(null=True, blank=True, verbose_name='Longitud de la Celebración')
    budget_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    couple_photo = models.ImageField(upload_to='events/%Y/%m/%d/', blank=True, null=True)
    design_template = models.CharField(max_length=20, choices=DESIGN_TEMPLATE_CHOICES, default='classic_romance', verbose_name='Diseño de Invitación')
    
    email_header = models.CharField(max_length=100, default='Estás invitado', verbose_name='Encabezado del correo')
    email_message = models.TextField(default='Nos llena de alegría compartir este momento tan especial contigo', verbose_name='Mensaje principal del correo')
    email_question = models.CharField(max_length=100, default='¿nos acompañarás?', verbose_name='Pregunta de confirmación')
    email_button_text = models.CharField(max_length=50, default='Confirmar Asistencia', verbose_name='Texto del botón')
    email_closing = models.CharField(max_length=100, default='Con amor', verbose_name='Cierre del correo')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'
        ordering = ['-date']
    
    def __str__(self):
        if self.bride_name and self.groom_name:
            return f'{self.bride_name} & {self.groom_name}'
        return self.name or 'Evento sin nombre'
    
    def save(self, *args, **kwargs):
        if self.bride_name and self.groom_name:
            self.name = f'{self.bride_name} & {self.groom_name}'
        if not self.slug:
            from django.utils.text import slugify
            base_slug = slugify(self.name) if self.name else 'evento'
            slug = base_slug
            counter = 1
            while Event.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
    
    @property
    def days_until(self):
        if not self.date:
            return 0
        delta = self.date - timezone.now().date()
        return max(0, delta.days)
    
    @property
    def total_guests(self):
        return self.guests.count()
    
    @property
    def confirmed_guests(self):
        return self.guests.filter(rsvp_status='CONFIRMED').count()
    
    @property
    def display_name(self):
        if self.bride_name and self.groom_name:
            return f'{self.bride_name} & {self.groom_name}'
        return self.name or 'Nuestra Boda'
    
    @property
    def has_valid_coordinates(self):
        if self.latitude is None or self.longitude is None:
            return False
        return abs(self.latitude) > 1.0 and abs(self.longitude) > 1.0
    
    @property
    def has_valid_celebration_coordinates(self):
        if self.celebration_latitude is None or self.celebration_longitude is None:
            return False
        return abs(self.celebration_latitude) > 1.0 and abs(self.celebration_longitude) > 1.0


class EventSchedule(models.Model):
    ICON_CHOICES = [
        ('church', 'Ceremonia'),
        ('restaurant', 'Recepción/Cena'),
        ('celebration', 'Fiesta'),
        ('cake', 'Pastel'),
        ('local_bar', 'Brindis'),
        ('photo_camera', 'Sesión de Fotos'),
        ('music_note', 'Música'),
        ('event', 'Otro'),
    ]
    
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='schedule')
    name = models.CharField(max_length=200)
    time = models.TimeField()
    venue = models.CharField(max_length=200)
    icon = models.CharField(max_length=50, choices=ICON_CHOICES, default='event')
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        verbose_name = 'Itinerario'
        verbose_name_plural = 'Itinerarios'
        ordering = ['order', 'time']
    
    def __str__(self):
        return f"{self.name} - {self.time.strftime('%H:%M')}"


class Guest(models.Model):
    RSVP_CHOICES = [
        ('PENDING', 'Pendiente'),
        ('CONFIRMED', 'Confirmado'),
        ('DECLINED', 'Rechazado'),
    ]
    
    MEAL_CHOICES = [
        ('STANDARD', 'Menú Estándar'),
        ('VEGETARIAN', 'Vegetariano'),
        ('VEGAN', 'Vegano'),
        ('CELIAC', 'Sin Gluten'),
    ]
    
    GROUP_CHOICES = [
        ('NOVIA', 'Familia de la Novia'),
        ('NOVIO', 'Familia del Novio'),
        ('AMIGOS_NOVIA', 'Amigos de la Novia'),
        ('AMIGOS_NOVIO', 'Amigos del Novio'),
        ('TRABAJO', 'Compañeros de Trabajo'),
        ('OTROS', 'Otros'),
    ]
    
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='guests')
    user = models.OneToOneField(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='guest_profile')
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    group = models.CharField(max_length=20, choices=GROUP_CHOICES)
    rsvp_status = models.CharField(max_length=20, choices=RSVP_CHOICES, default='PENDING')
    meal_choice = models.CharField(max_length=20, choices=MEAL_CHOICES, default='STANDARD')
    plus_one = models.BooleanField(default=False)
    plus_one_name = models.CharField(max_length=200, blank=True)
    linked_to = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='plus_ones')
    notes = models.TextField(blank=True)
    assigned_table = models.ForeignKey('Table', on_delete=models.SET_NULL, null=True, blank=True, related_name='guests')
    invitation_token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    token_created_at = models.DateTimeField(null=True, blank=True)
    invitation_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Invitado'
        verbose_name_plural = 'Invitados'
        ordering = ['full_name']
    
    def __str__(self):
        return self.full_name

    def get_plus_one(self):
        return self.plus_ones.first()


class Table(models.Model):
    SHAPE_CHOICES = [
        ('CIRCULAR', 'Circular'),
        ('RECTANGULAR', 'Rectangular'),
    ]
    
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='tables')
    name = models.CharField(max_length=100)
    capacity = models.IntegerField(default=8)
    shape = models.CharField(max_length=20, choices=SHAPE_CHOICES, default='CIRCULAR')
    position_x = models.FloatField(default=0)
    position_y = models.FloatField(default=0)
    is_head_table = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Mesa'
        verbose_name_plural = 'Mesas'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    @property
    def assigned_guests_count(self):
        return self.guests.count()
    
    @property
    def available_seats(self):
        return self.capacity - self.assigned_guests_count

    def get_main_guests(self):
        plus_one_ids = self.guests.filter(linked_to__isnull=False).values_list('pk', flat=True)
        return self.guests.exclude(pk__in=plus_one_ids)


class Photo(models.Model):
    CATEGORY_CHOICES = [
        ('PREPARATIVES', 'Preparativos'),
        ('CEREMONY', 'Ceremonia'),
        ('RECEPTION', 'Recepción'),
        ('OTHER', 'Otros'),
    ]
    
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='photos')
    uploaded_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='uploaded_photos')
    image = models.ImageField(upload_to='photos/%Y/%m/%d/')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='OTHER')
    caption = models.CharField(max_length=300, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Foto'
        verbose_name_plural = 'Fotos'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.event.name} - {self.caption[:30]}"


class ChecklistItem(models.Model):
    PRIORITY_CHOICES = [
        ('HIGH', 'Alta'),
        ('MEDIUM', 'Media'),
        ('LOW', 'Baja'),
    ]
    
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='checklist_items')
    title = models.CharField(max_length=300)
    is_completed = models.BooleanField(default=False)
    due_date = models.DateField(null=True, blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='MEDIUM')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Tarea'
        verbose_name_plural = 'Lista de Tareas'
        ordering = ['priority', 'due_date']
    
    def __str__(self):
        return self.title


class BudgetItem(models.Model):
    CATEGORY_CHOICES = [
        ('VENUE', 'Lugar'),
        ('CATERING', 'Catering'),
        ('ATTIRE', 'Vestuario'),
        ('PHOTOGRAPHY', 'Fotografía'),
        ('FLOWERS', 'Flores'),
        ('MUSIC', 'Música'),
        ('TRANSPORT', 'Transporte'),
        ('OTHER', 'Otros'),
    ]
    
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='budget_items')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.CharField(max_length=300)
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    actual_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    class Meta:
        verbose_name = 'Item de Presupuesto'
        verbose_name_plural = 'Presupuesto'
        ordering = ['category']
    
    def __str__(self):
        return f"{self.category} - {self.description}"
    
    @property
    def difference(self):
        return self.estimated_cost - self.actual_cost
