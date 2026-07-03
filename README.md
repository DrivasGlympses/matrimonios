# Ethereal Union - Wedding Management System

Sistema de gestión de bodas construido con Django.

## Características

- **Dashboard**: Panel de control con countdown, estadísticas RSVP, checklist y presupuesto
- **Plan de Mesas**: Gestión visual e interactiva de mesas con drag & drop (SortableJS)
- **Galería**: Álbum de fotos colaborativo con subida de imágenes
- **Página Pública**: Invitación digital con formulario RSVP funcional
- **Sistema de Autenticación**: Roles separados para Wedding Planners e Invitados

## Requisitos

- Python 3.10+
- pip

## Instalación

1. **Crear entorno virtual**:
```bash
python -m venv venv
```

2. **Activar entorno virtual**:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Instalar dependencias**:
```bash
pip install -r requirements.txt
```

4. **Ejecutar migraciones**:
```bash
python manage.py migrate
```

5. **Crear superusuario**:
```bash
python manage.py createsuperuser
```

6. **Cargar datos de ejemplo** (opcional):
```bash
python manage.py create_sample_data
```

7. **Ejecutar servidor**:
```bash
python manage.py runserver
```

8. **Abrir en navegador**:
- Panel de administración: http://localhost:8000/admin/
- Página pública: http://localhost:8000/
- Dashboard: http://localhost:8000/dashboard/

## Credenciales de prueba

```
Usuario: admin
Email: admin@ethereal.com
Contraseña: admin123
```

## Estructura del proyecto

```
matrimonios/
├── apps/
│   ├── core/          # Modelos, auth, admin
│   ├── dashboard/     # Panel de control
│   ├── tables/        # Gestión de mesas
│   ├── gallery/       # Galería de fotos
│   └── event/         # Página pública y RSVP
├── templates/         # Templates HTML
├── static/           # CSS, JS, imágenes
├── media/            # Archivos subidos
└── ethereal_union/   # Configuración Django
```

## Modelos principales

- **Event**: Información del evento (nombre, fecha, ubicación, presupuesto)
- **Guest**: Invitados con RSVP, preferencias de menú, grupo
- **Table**: Mesas con posición, capacidad y forma
- **Photo**: Fotos de la galería
- **ChecklistItem**: Tareas del wedding planner
- **BudgetItem**: Items del presupuesto

## URLs principales

| Ruta | Descripción |
|------|-------------|
| `/` | Página pública del evento |
| `/rsvp/` | Formulario de confirmación |
| `/dashboard/` | Panel de control (requiere login) |
| `/tables/` | Plan de mesas (requiere login) |
| `/gallery/` | Galería de fotos |
| `/admin/` | Panel de administración |

## Diseño

El sistema utiliza el design system "Ethereal Union" basado en:
- **Tipografía**: Playfair Display + Inter
- **Colores**: Blush (#6b5a5f), Champagne Gold (#D4AF37)
- **Estilo**: Modern Editorial con "Whisper Shadow"
