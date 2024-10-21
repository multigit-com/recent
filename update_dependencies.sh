#!/bin/bash

echo "Updating Python dependencies..."
pip install --upgrade -r requirements.txt

echo "Updating webdriver-manager..."
pip install --upgrade webdriver-manager

echo "Dependencies updated. Please restart the script."
