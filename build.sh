#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py migrate

# Crea el superusuario si las variables de entorno existen y el usuario no
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
import os

User = get_user_model()
username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

if username and password and not User.objects.filter(username=username).exists():
    email = os.environ.get('DJANGO_SUPERUSER_EMAIL', '')
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"Superusuario '{username}' creado.")
else:
    print(f"Superusuario '{username}' ya existe o no se definieron las variables, omitiendo creación.")
EOF