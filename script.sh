#!/bin/bash

# Update the package index
sudo apt update

# Install the venv module for Python 3
sudo apt install python3-venv

# Create a virtual environment named 'my_venv'
python3 -m venv my_venv

# Activate the virtual environment
source my_venv/bin/activate

pip3 install -r requirements.txt

jupyter lab

# Ilya Sutskever