#!/bin/bash
set -e

pip install -r requirements.txt
python manage.py migrate

# Optional: bootstrap Django admin user on each deploy.
# Set DJANGO_SUPERUSER_USERNAME / DJANGO_SUPERUSER_EMAIL / DJANGO_SUPERUSER_PASSWORD
# in Render environment variables.
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_EMAIL" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
  python manage.py shell -c "from django.contrib.auth import get_user_model; U=get_user_model(); u,created=U.objects.get_or_create(username='$DJANGO_SUPERUSER_USERNAME', defaults={'email':'$DJANGO_SUPERUSER_EMAIL'}); u.email='$DJANGO_SUPERUSER_EMAIL'; u.is_staff=True; u.is_superuser=True; u.set_password('$DJANGO_SUPERUSER_PASSWORD'); u.save(); print('superuser created' if created else 'superuser updated')"
fi

python manage.py collectstatic --noinput
