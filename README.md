virtualenv env
source env/bin/activate
pip install -r requirements.txt
cd SimpleTodo/
python manage.py migrate
python manage.py createsuperuser --email admin@example.com --username admin
python manage.py runserver


cd FrontEnd/
python -m SimpleHTTPServer 8080

Go to http://0.0.0.0:8080/