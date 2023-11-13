# labvalues-api

## Environments

### Run labtest-api in virtual environment venv 

```
python3 -m venv venv 
source ./venv/bin/activate
pip install -r requirements.txt
```
This is how you run the code locally (without Docker):

```
uvicorn app.src.main:app --host 0.0.0.0 --port 8080 --reload
```
### Run labtest-api in Docker 
As a first step, install Docker (see: https://www.docker.com) and install the requirements:
Build and run the Docker image locally, as follows:

```
docker build -t labvalues-api .
docker run -d -p 8080:80 labvalues-api
```

In order to run the example server with docker compose, use this:

```
docker-compose up --build
```

If you use docker compose and you make a minor change in the file, you can now see how everything is updated and the server is restarted automatically.

## Usage

Access labtest-api [OpenAPI (Swagger)](https://swagger.io/specification/) docs via
```
http://localhost:8080/docs
```
and [Redoc](https://github.com/Redocly/redoc) via
```
http://localhost:8080/redoc
```