#!/bin/bash
set -e

pip install -r requirements.txt
python manage.py migrate

python manage.py shell -c "from django.contrib.auth import get_user_model; U=get_user_model(); u,created=U.objects.get_or_create(username='burminho', defaults={'email':'burminho098@gmail.com'}); u.email='burminho098@gmail.com'; u.is_staff=True; u.is_superuser=True; u.set_password('12345'); u.save(); print('superuser created' if created else 'superuser updated')"

python manage.py collectstatic --noinput
