#!/bin/bash
python manage.py migrate --noinput
python create_superuser.py
