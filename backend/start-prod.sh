#!/bin/bash

export DJANGO_SETTINGS_MODULE=fyp.settings.prod
gunicorn fyp.wsgi