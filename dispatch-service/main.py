from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI, Depends
import docker

logging.basicConfig(level=logging.INFO)

@asynccontextmanager
async def lifespan(_app: FastAPI):
    _cli = docker.DockerClient(base_url="unix:///var/run/docker.sock")

    try:
        _containers = [container.name for container in _cli.containers.list(filters={"ancestor": "taxi-zone-worker-service"}, all=True)]
        logging.info(f"containers: {_containers}")
        yield
    finally:
        pass

app = FastAPI(title="Taxi Zone API", version="0.1.0", lifespan=lifespan)

# app.include_router()
