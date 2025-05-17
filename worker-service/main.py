import anyio
import os
import logging
import socket
from whenever import Instant
import httpx

logging.basicConfig(level=logging.INFO)


async def worker_task():
    current_time = Instant.now().py_datetime().strftime("%Y%m%d")
    logging.info(f"Worker running at {current_time} | PID: {str(os.getpid())} {str(socket.gethostname())}")
    await anyio.sleep(2.0)
    _trip = httpx.get(f"http://dispatch-service:8000/api/v1/trips/{str(socket.gethostname())}").json()
    if not _trip:
        logging.info(f"No trip found for this worker {str(socket.gethostname())}")
        return
    logging.info(f"Trip details: {_trip}")
    await anyio.sleep(2.0)
    httpx.patch(f"http://dispatch-service:8000/api/v1/trips/{_trip["trip_id"]}", params={"status": "picking_up"})
    await anyio.sleep(2.0)
    httpx.patch(f"http://dispatch-service:8000/api/v1/trips/{_trip["trip_id"]}", params={"status": "in_progress"})
    await anyio.sleep(2.0)
    httpx.patch(f"http://dispatch-service:8000/api/v1/trips/{_trip["trip_id"]}", params={"status": "completed"})
    await anyio.sleep(2.0)


async def main():
    logging.info("Starting taxi worker service...")
    await worker_task()


if __name__ == "__main__":
    anyio.run(main)
