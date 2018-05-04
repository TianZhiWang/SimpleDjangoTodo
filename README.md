# Setting Up

## Running Backend
```
virtualenv env
source env/bin/activate
pip install -r requirements.txt
cd SimpleTodo/
python manage.py migrate
python manage.py createsuperuser --email admin@example.com --username admin
python manage.py runserver
```
## Running Frontend
```
cd FrontEnd/
python -m SimpleHTTPServer 8080
```
## View App
Go to http://0.0.0.0:8080/  
Login with user created

## Testing
```
cd SimpleTodo/
python manage.py test
```