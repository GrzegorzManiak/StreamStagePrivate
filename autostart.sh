#!/bin/bash

# Navigate to StreamStagePrivate directory
echo "Navigating to /home/ubuntu/StreamStagePrivate directory..."
cd /home/ubuntu/StreamStagePrivate || exit

# Create a Python virtual environment if it doesn't already exist
if [ ! -d "env" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv env
fi

# Activate the Python virtual environment
echo "Activating Python virtual environment..."
source env/bin/activate

# Install PIP packages if not already installed
echo "Installing PIP packages..."
pip install -r requirements.txt

# Pull changes from main branch and merge into server branch
echo "Pulling changes from main branch and merging into server branch..."
git checkout server
git pull origin main
git push origin server

# Make migrations for specified apps
echo "Making migrations for specified apps..."
apps='accounts applications events orders store search StreamStage'
for app in $apps
do
    echo "Making migrations for $app..."
    python3 App/manage.py makemigrations "$app"
    echo ""
done

# Migrate database
echo "Migrating database..."
python3 App/manage.py migrate

# Push changes to media and db.sqlite3 files/folders
echo "Pushing changes to media and db.sqlite3 files/folders..."
git add App/media
git add App/db.sqlite3
git commit -m "Changes made to media and db.sqlite3 files/folders"
git push origin server

# Start server on 0.0.0.0:80
echo "Starting server on 0.0.0.0:80..."
nohup python3 App/manage.py runserver 0.0.0.0:80 > django.log 2>&1 &
