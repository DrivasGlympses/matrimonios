# AGENTS.md

## Project Overview

Django 6.0 wedding management system ("Ethereal Union"). Spanish-language UI.

## Dev Commands

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py create_sample_data  # loads sample event/guests
python manage.py runserver
```

## Testinga
## Testinga


```bash
python manage.py test [appname]   # e.g. python manage.py test apps.dashboard
```

No pytest config — uses Django's built-in test runner.

## Key Architecture

- **CustomUser**: `apps.core.models.CustomUser` (extends AbstractUser, has `role` field: PLANNER/GUEST)
- **Auth URLs**: `/accounts/login/`, `/accounts/logout/`, `/accounts/signup/`
- **App namespace pattern**: all apps live under `apps/` (e.g. `apps.dashboard`, `apps.event`)
- **AUTH_USER_MODEL**: `core.CustomUser`
- **DB**: SQLite at `db.sqlite3`

## Design System

Design rules at `design-system/ethereal-union/MASTER.md` override defaults:
- Primary `#DB2777`, Secondary `#F472B6`, CTA/Accent `#CA8A04`
- Fonts: **Playfair Display** (headings) + **Inter** (body)
- Shadow levels: `--shadow-sm` through `--shadow-xl`
- **Anti-patterns**: No emojis as icons (use SVG), all clickables need `cursor-pointer`

## URL Routes

| Path | App | Notes |
|------|-----|-------|
| `/` | event | Public invitation page |
| `/rsvp/` | event | RSVP form |
| `/dashboard/` | dashboard | Requires login |
| `/tables/` | tables | Seat planning, requires login |
| `/gallery/` | gallery | Photo album |
| `/admin/` | — | Django admin |

## Quirks

- Templates in `templates/` (not inside apps)
- Media files in `media/photos/` and `media/events/`
- `django-extensions` and `crispy-tailwind` installed
- Spanish UI throughout (`LANGUAGE_CODE = 'es'`)
- Tests in `apps/*/tests.py` are empty stubs
-prueba
