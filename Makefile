parsecountry:
	docker exec django_backend python manage.py parsecountry

makemigration:
	docker exec django_backend python manage.py makemigration

migrate:
	docker exec django_backend python manage.py migrate