# fhirlab

## Environments

### Run fhirlab in virtual environment venv 

```
python3 -m venv venv 
source ./venv/bin/activate
pip install -r requirements.txt
```
This is how you run the code locally (without Docker):

```
uvicorn backend.src.main:app --host 0.0.0.0 --port 8000 --reload
```
### Run fhirlab in Docker 
As a first step, install Docker (see: https://www.docker.com) and install the requirements:
Build and run the Docker image locally, as follows:

```
docker build -t fhirlab .
docker run -d -p 8000:80 fhirlab
```

In order to run the example server with docker compose, use this:

```
docker-compose up --build
```

If you use docker compose and you make a minor change in the file, you can now see how everything is updated and the server is restarted automatically.

## Usage

Access fhirlab [OpenAPI (Swagger)](https://swagger.io/specification/) docs via
```
http://localhost:8000/api/docs
```
and [Redoc](https://github.com/Redocly/redoc) via
```
http://localhost:8000/api/redoc
```
and [OpenAPI document ](https://swagger.io/specification) via
```
http://localhost:8000/api/openapi.json
```
