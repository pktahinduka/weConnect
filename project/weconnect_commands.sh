#!/bin/sh

set APP_SETTINGS=project.config.DevelopmentConfig
set DATABASE_URL=postgres://postgres:peter926@localhost:5432/users_dev
set DATABASE_TEST_URL=postgres://postgres:peter926@localhost:5432/users_test
set SECRET_KEY=change_me
python manage.py runserver -p 5555