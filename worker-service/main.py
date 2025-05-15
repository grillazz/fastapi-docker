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

async def main():
    logging.info("Starting taxi worker service...")
    await worker_task()

if __name__ == "__main__":
    anyio.run(main)