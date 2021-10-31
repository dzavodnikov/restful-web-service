# Build container
FROM python:3.6.15-bullseye

# Start container
RUN mkdir -p /usr/share/rest
WORKDIR /usr/share/rest

COPY src/*.py ./

COPY requirements.txt ./
RUN python -m pip install -r requirements.txt

ENTRYPOINT ["uvicorn", "main:app", "--app-dir", "/usr/share/rest", "--host", "0.0.0.0"]
