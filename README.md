# FLASK BACKEND TEMPLATE

## Install Vscode Extensions
```
pylance
```


## Switch to virtual environment
```bash
virtualenv venv
source venv/Script/activate
```

## Install Dependencies
```bash
yarn
```

```bash
pip install -r requirements.txt

pip install `your want to install`

pip freeze > requirements.txt
```

## Start Development
```bash
# start development server
flask run
```

## Play with Shell
```bash
flask shell
```

## Migrate Database
```bash
# Init Database
flask db init

flask db migrate -m "your comment"

flask db upgrade
```

## Init Database
```bash
flask init-db
```

## Deploy
```bash
docker-compose up
```

## Commit Message
see https://www.conventionalcommits.org/en/v1.0.0/

## Other
flask-sqlalchemy-stubs==0.0.1