import argparse
import asyncio
from server_async.server import start_async_server
from server_sync.server import start_sync_server


def main():
    parser = argparse.ArgumentParser(description="TP2 - Image Processing")
    parser.add_argument("-i", "--ip", required=True, help="Async server listening address")
    parser.add_argument("-p", "--port", required=True, type=int, help="Async server listening port")
    args = parser.parse_args()

    # Start the sync server in a separate process
    start_sync_server()

    # Start the async server with the provided IP and port
    asyncio.run(start_async_server(args.ip, args.port))


if __name__ == "__main__":
    main()