import random
from contextlib import asynccontextmanager
import logging

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy import text
from fastapi import FastAPI
import docker
from .database import get_db
from .model import Taxi
from .api import router as api_router

logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    _app.docker_cli = docker.DockerClient(base_url="unix:///var/run/docker.sock")

    _app.db_session = await anext(get_db())

    try:
        _containers = [
            container.short_id
            for container in _app.docker_cli.containers.list(
                filters={"ancestor": "taxi-zone-worker-service"}, all=True
            )
        ]
        _taxis = [
            Taxi(taxi_id=_container, x=random.randint(0, 100), y=random.randint(0, 100))
            for _container in _containers
        ]

        try:
            # truncate the taxis table
            await _app.db_session.execute(text("TRUNCATE taxis CASCADE"))
            _app.db_session.add_all(_taxis)
            await _app.db_session.commit()
        except IntegrityError as ex:
            await _app.db_session.rollback()
            logging.warning(f"Skipping taxi insertion due to integrity error: {ex}")

        logging.info(f"db_session: {_app.db_session}")
        logging.info(f"containers: {_containers}")
        yield
    finally:
        _app.db_session.close()
        _app.docker_cli.close()


app = FastAPI(title="Taxi Zone API", version="0.1.0", lifespan=lifespan)

app.include_router(api_router, prefix="/api/v1", tags=["v1"])
