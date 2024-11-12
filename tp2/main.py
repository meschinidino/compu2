import multiprocessing
import asyncio
import logging
import time
import argparse
from tp2.server_sync.server import start_sync_server
from tp2.server_async.server import start_async_server

logging.basicConfig(level=logging.INFO)

async def start_servers():
    sync_server_process = multiprocessing.Process(target=start_sync_server)
    sync_server_process.start()
    time.sleep(5)
    await start_async_server('::', 8000)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start the servers.")
    args = parser.parse_args()
    asyncio.run(start_servers())