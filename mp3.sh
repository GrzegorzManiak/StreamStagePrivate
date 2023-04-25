#!/bin/bash
echo ""
echo "WOULD YOU LIKE TO DELETE YOUR MIGRATIONS?"
echo ""
while true; do
    read -p "[y/n] > " yn
    case $yn in 
        [Yy]* ) 
            echo "Deleting existing migrations..."
            echo ""
            find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
            find . -path "*/migrations/*.pyc" -delete
            echo ""
            echo "Deleting complete."
            echo ""
            break
            ;;
        [Nn]* ) 
            echo ""
            break
            ;;
        * ) 
            echo "Please answer Y or N."
            ;;
    esac
done

echo ""
echo "WOULD YOU LIKE TO DELETE YOUR DATABASE?"
echo ""

while true; do
    read -p "[y/n] > " yn
    case $yn in
        [Yy]* ) 
            echo "Deleting Database..."
            if [ -f "App/db.sqlite3" ]; then
                rm App/db.sqlite3
            else
                echo "Database file does not exist."
            fi
            echo ""
            break
            ;;
        [Nn]* ) 
            echo ""
            break
            ;;
        * ) 
            echo "Please answer Y, or N."
            ;;
    esac
done

echo ""
echo "Making migrations..."
echo ""

apps="accounts applications events orders store search StreamStage"

for i in $apps; do
    python App/manage.py makemigrations $i
    echo ""
done

echo "Migrating..."
echo ""

python App/manage.py migrate

echo ""
echo "WOULD YOU LIKE TO CREATE A SUPERUSER WITH DEFAULT PARAMETERS?"
echo ""

while true; do
    read -p "[y/n] > " yn
    case $yn in
        [Yy]* ) 
            echo "Creating superuser..."
            python App/manage.py createsuperuser --username=admin --email=admin@example.com --first_name=Admin --last_name=Admin
            echo ""
            break
            ;;
        [Nn]* ) 
            echo ""
            break
            ;;
        * ) 
            echo "Please answer Y or N."
            ;;
    esac
done

read -p "Press any key to continue..."
