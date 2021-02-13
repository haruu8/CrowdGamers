psql:
	docker-compose exec postgres psql -U django_db_user -p 5432 -h 0.0.0.0 -d django_db
migrate:
	docker-compose exec django python3 manage.py migrate --run-syncdb
migrations:
	docker-compose exec django python3 manage.py makemigrations
migrations-clans:
	docker-compose exec django python3 manage.py makemigrations clans
migrations-accounts:
	docker-compose exec django python3 manage.py makemigrations accounts
createsuperuser:
	docker-compose exec django python3 manage.py createsuperuser
showmigrations:
	docker-compose exec django python3 manage.py showmigrations
test:
	docker-compose exec django python3 manage.py test
insert-data-feature:
	docker-compose exec django python3 manage.py loaddata feature_initial.json
insert-data-game:
	docker-compose exec django python3 manage.py loaddata game_initial.json
insert-data-question:
	docker-compose exec django python3 manage.py loaddata question_initial.json