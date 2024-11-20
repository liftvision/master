#!/bin/bash

./manage.py makemigration
./manage.py migrate
./manage.py collectstatic
./manage.py runserver --insecure 0.0.0.0:8000
