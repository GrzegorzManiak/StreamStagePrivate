#!/bin/bash

# array of Django apps to migrate
apps=("accounts" "applications" "server_manager" "stream")

# go into the App directory
cd App

# loop over apps and run migrate command
for app in "${apps[@]}"
do
    echo "Migrating $app"
    python manage.py makemigrations "$app"

python manage.py migrate
cd ..

done