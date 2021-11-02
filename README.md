# Description

This is simple example of RESTful Web Service on Python.

# How to run

 1. Install required packages:
```
$ python -m pip install -r requirements.txt
```
 2. Run:
```
$ uvicorn rest_app.rest:app --app-dir src --host 0.0.0.0 --reload
```
To see Web UI go to [http://localhost:8000](http://localhost:8000).

Swagger UI available at [http://localhost:8000/docs](http://localhost:8000/docs).

 3. Unit-tests:
```
$ pytest --rootdir=src -v src/tests/rest.py
```

# How to use in Docker

1) Build Docker image. In root directory run:

```
$ docker-compose -f ./docker/docker-compose.yml build
```

2) Run Docker containers with application:

```
$ docker-compose -f ./docker/docker-compose.yml up
```

3) Open Web UI at [http://localhost:18000](http://localhost:18000) or 
Swagger UI at [http://localhost:18000/docs](http://localhost:18000/docs).

_Note:_
To stop run:

```
$ docker-compose -f ./docker/docker-compose.yml down
```
