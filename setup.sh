#!/bin/bash

echo "Installing required Python packages..."
pip install -r requirements.txt

echo "Checking if django_filters is installed correctly..."
python -c "import django_filters; print(f'django_filters version {django_filters.__version__} installed successfully')"

chmod +x /root/MarcioMiguel22/Sites/Test02/setup.sh

echo "Setup completed."

./setup.sh

gunicorn backend.wsgi:application
