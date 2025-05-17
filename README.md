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