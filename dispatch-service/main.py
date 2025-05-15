import random
from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI, Depends
import docker
from .database import get_db
from .model import Taxi

logging.basicConfig(level=logging.INFO)



@asynccontextmanager
async def lifespan(_app: FastAPI):
    _cli = docker.DockerClient(base_url="unix:///var/run/docker.sock")

    _app.db_session = await anext(get_db())

    try:
        _containers = [container.name for container in _cli.containers.list(filters={"ancestor": "taxi-zone-worker-service"}, all=True)]
        _taxis = [Taxi(taxi_id=_container, x=random.randint(0, 100), y=random.randint(0, 100)) for _container in _containers]
        # TODO: sqlalchemy.exc.IntegrityError: (sqlalchemy.dialects.postgresql.asyncpg.IntegrityError)
        #  <class 'asyncpg.exceptions.UniqueViolationError'>: duplicate key value violates unique constraint "taxis_pkey"
        _app.db_session.add_all(_taxis)
        await _app.db_session.commit()

        logging.info(f"db_session: {_app.db_session}")
        logging.info(f"containers: {_containers}")
        yield
    finally:
        pass


app = FastAPI(title="Taxi Zone API", version="0.1.0", lifespan=lifespan)

# app.include_router()
