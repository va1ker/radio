parsecountry:
	docker exec django_backend python manage.py parsecountry

parsestations:
	docker exec django_backend python manage.py parsestations

makemigrations:
	docker exec django_backend python manage.py makemigrations

migrate:
	docker exec django_backend python manage.py migrate

