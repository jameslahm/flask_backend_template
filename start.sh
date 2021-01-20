nginx
export FLASK_APP='main'
export FLASK_ENV='production'
flask init-db
uwsgi --ini uwsgi.ini
