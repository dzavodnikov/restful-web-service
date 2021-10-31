# Build container
FROM python:3.6.15-bullseye

# Start container
COPY data               /usr/share/data
COPY src/rest_app       /usr/share/rest_app
COPY requirements.txt   /usr/share/rest_app

WORKDIR /usr/share
RUN python -m pip install -r rest_app/requirements.txt
ENTRYPOINT ["uvicorn", "rest_app.rest:app", "--app-dir", "/usr/share", "--host", "0.0.0.0"]
