psql:
	docker-compose exec postgres psql -U django_db_user -p 5432 -h 0.0.0.0 -d django_db
migrate:
	docker-compose exec django python3 manage.py migrate --run-syncdb
migrations:
	docker-compose exec django python3 manage.py makemigrations
migrations-teams:
	docker-compose exec django python3 manage.py makemigrations teams
migrations-accounts:
	docker-compose exec django python3 manage.py makemigrations accounts
user:
	docker-compose exec django python3 manage.py createsuperuser
showmigrations:
	docker-compose exec django python3 manage.py showmigrations
static:
	docker-compose exec django python3 manage.py collectstatic
test:
	docker-compose exec django python3 manage.py test
testdc:
	docker-compose up -d \
	&& docker-compose exec django python3 manage.py test \
	&& docker-compose down
coverage-test:
	docker-compose exec django coverage run --source='.' manage.py test
report:
	docker-compose exec django coverage report
html:
	docker-compose exec django coverage html
insert:
	docker-compose exec django python3 manage.py loaddata user_initial.json \
	&& docker-compose exec django python3 manage.py loaddata feature_initial.json \
	&& docker-compose exec django python3 manage.py loaddata game_initial.json \
	&& docker-compose exec django python3 manage.py loaddata question_initial.json \
	&& docker-compose exec django python3 manage.py loaddata job_initial.json
insert-user:
	docker-compose exec django python3 manage.py loaddata user_initial.json
insert-sample-data:
	docker-compose exec django python3 manage.py loaddata sample_user_initial.json
insert-feature:
	docker-compose exec django python3 manage.py loaddata feature_initial.json
insert-game:
	docker-compose exec django python3 manage.py loaddata game_initial.json
insert-faq:
	docker-compose exec django python3 manage.py loaddata question_initial.json
insert-job:
	docker-compose exec django python3 manage.py loaddata job_initial.json
