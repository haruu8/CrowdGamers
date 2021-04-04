#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $DATABASE_HOST $DATABASE_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python3 manage.py flush --no-input
python3 manage.py migrate --run-syncdb
python3 manage.py collectstatic --no-input --clear
python3 manage.py loaddata user_initial.json
python3 manage.py loaddata feature_initial.json
python3 manage.py loaddata game_initial.json
python3 manage.py loaddata question_initial.json
python3 manage.py loaddata job_initial.json

exec "$@"