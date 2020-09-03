# grafitrol-shoot-service

## Setup App
Run the following commands:

- Ensure you have `Python 3.7.2`  installed from [here](https://www.python.org/downloads/release/python-372/)
- Install `pipenv` via: 
```bash
pip install pipenv
```
- Clone repo via:  
```bash
git clone https://github.com/veeqtor/grafitrol-shoot-service.git
```
- Start virtual environment via:
```bash
pipenv shell
```
- Install dependencies via:
```bash
pipenv install
```
- Make bash scripts executable via:
```bash
chmod +x scripts/install_hooks.sh scripts/pre_commit.sh
```
- Install hooks by running:
```bash
scripts/install_hooks.sh
```

- Use the `.env-sample` file to create a `.env` file with required environmental variables

- Generate migration
```bash
flask db migrate -m <name_of_migration>
```

- Run migrations
```bash
flask db upgrade
```

- Run lint manually
```bash
yapf -ir $(find . -name '*.py')
```

#### Setup app with Docker
- Ensure you have [Docker for mac](https://docs.docker.com/docker-for-mac/install/) installed and running on your machine

- Build and tag the docker image
```bash
docker build -t <tag> -f Docker/Dockerfile .
```

- Spin up the container
```bash
docker run -d --name <container name> --env FLASK_ENV='<environment>' --env DATABASE_URL='<database url>' -p 5000:5000  <tag>:latest
```

- The above command should return a container ID, to stop a running container
```bash
 docker stop <containerID>
```
OR
```bash
 docker stop <container name>
```

## Redis and Celery
Celery is used as the message broker for the API. We use it to run heavy task(via celery-workers) and run cron-jobs(via celery-beat).

#### Starting Redis
In order to run celery, you would need to ensure that a `redis` is running. 
Using docker, you can achieve this by running 

```bash
docker run -p 6379:6379 redis
``` 
This would spin up a redis server in  port `6379` in your machine.

If your `redis server` is running on a different port/host, you must specify the URL in the `.env` file via key `REDIS_SERVER_URL`

#### Starting Celery
Once Redis is up and running, you can now spin up celery in these steps:

- Start celery worker by executing 

```bash
celery -A  celery_config.celery_app worker --loglevel=info
```
- In a separate terminal, spin up the celery beat via
