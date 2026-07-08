#!/bin/bash
set -e

echo "Aplicando migraciones..."
python manage.py migrate --noinput

echo "Recolectando archivos estaticos..."
python manage.py collectstatic --noinput

echo "Iniciando servidor..."
exec "$@"
