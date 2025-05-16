import anyio
import os
import logging

from whenever import Instant

logging.basicConfig(level=logging.INFO)


async def worker_task():
    # while True:
    current_time = Instant.now().py_datetime().strftime("%Y%m%d")
    logging.info(f"Worker running at {current_time} | PID: {str(os.getpid())}")
    await anyio.sleep(2.0)
    # get trip details from the database
    # start drive post to start router and set taxi busy
    # await anyio.sleep(2.0)
    # await anyio.sleep(2.0)
    # stop drive post to stop router and set taxi available and update position fo the taxi with x_end and y_end


async def main():
    logging.info("Starting taxi worker service...")
    await worker_task()


if __name__ == "__main__":
    anyio.run(main)
