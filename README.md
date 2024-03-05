# Lucky Numberz  
Lottery Numbers Generator  
A web app written in Python 3 using Django framework  

## About
This is a personal portfolio project written in Python which uses the Python web framework Django and is distributed under MIT License. For simplicity it runs using the own SQLite.  

## Running (only for development or testing)
The application deployment should be made using a proper web server compatible with WSGI or ASGI. For a deployment-ready configuration see [lottery-ticket](https://github.com/LucasKodex/lottery-ticket) repository.

### Linux

1. `python3 -m venv venv`
1. `source venv/bin/activate`
1. `python3 -m pip install -r requirements.txt`
1. `python3 manage.py migrate`
1. `python3 manage.py runserver` (only should be used for development and testing)

### Windows

1. `python3 -m venv venv`
1. `venv/bin/activate.bat`
1. `python3 -m pip install -r requirements.txt`
1. `python3 manage.py migrate`
1. `python3 manage.py runserver` (only should be used for development and testing)

