createvenv:
	python3 -m venv venv

activate:
	source venv/bin/activate

dep:
	pip3 install -r requirements.txt

run:
	python3 manage.py runserver

superuser:
	python3 manage.py createsuperuser


migrationsfile:
	python3 manage.py makemigrations

migration:
	python3 manage.py migrate

django:
	pip3 install django