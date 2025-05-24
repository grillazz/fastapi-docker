# Autonomous Taxi Services Zone

This project implements a microservices-based taxi dispatch system using 
Python, FastAPI, SQLAlchemy, and Docker. 
It consists of a dispatch service that manages taxi assignments and trip statuses,
and worker services that simulate taxi operations.
The system supports dynamic taxi allocation, trip lifecycle management,
and real-time status updates via RESTful APIs.

Main features:
- FastAPI-based dispatch API for trip creation and status updates
- Asynchronous worker services representing taxis
- Docker integration for managing taxi worker containers
- SQL database for persistent storage of taxis and trips


### 1. install uv

### 2. uv sync
this will crate a virtual environment and install all dependencies

### 3. make docker-build
this will build the docker image

### 4. make docker-apply-db-migrations
this will apply the database migrations

### 5. make docker-up
this will start the docker container

### register trip
```shell
curl -X 'POST' \
  'http://0.0.0.0:8000/api/v1/trips' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "user_id": "string",
  "start_x": 71,
  "start_y": 22,
  "end_x": 3,
  "end_y": 4
}'
```
and get response
```json
{
  "trip_id": 8,
  "taxi_id": "a8a3fcb445e5",
  "status": "assigned"
}
```
