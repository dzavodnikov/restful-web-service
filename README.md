# Description

This is simple example of RESTful Web Service on Python.

# How to run

 1. Install required packages:
```
$ python -m pip install -r requirements.txt
```
 2. Run:
```
$ uvicorn main:app --app-dir src --reload
```
To see the result go to [http://127.0.0.1:8000](http://127.0.0.1:8000).

SwaggerUI available at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

# How to use in Docker

1) Build Docker image. In root directory run:

```
$ docker-compose build
```

2) Run Docker containers with application:

```
$ docker-compose up
```

3) Open `http://localhost:18000/`.

_Note:_
To stop run:

```
$ docker-compose down
```
