psql:
	docker-compose exec postgres psql -U django_db_user -p 5432 -h 0.0.0.0
migrate:
	docker-compose exec django python3 manage.py migrate --run-syncdb
migrations:
	docker-compose exec django python3 manage.py makemigrations
createsuperuser:
	docker-compose exec django python3 manage.py createsuperuser