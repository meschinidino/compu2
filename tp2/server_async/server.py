import asyncio
from PIL import Image
import io
import logging

logging.basicConfig(level=logging.INFO)

async def send_to_sync_server(image_data):
    reader, writer = await asyncio.open_connection('localhost', 8888)
    writer.write(image_data)
    await writer.drain()

    scaled_image_data = await reader.read(10000)
    writer.close()
    await writer.wait_closed()
    return scaled_image_data

async def handle_client(reader, writer):
    logging.info("Received request to process image")
    data = b""
    while True:
        chunk = await reader.read(10000)
        if not chunk:
            break
        data += chunk
        logging.info(f"Received {len(chunk)} bytes, total {len(data)} bytes")

        # Process the image once all data is received
        if len(chunk) < 10000:
            try:
                # Convert image to grayscale
                image = Image.open(io.BytesIO(data)).convert("L")
                output = io.BytesIO()
                image.save(output, format='JPEG')
                grayscale_image_data = output.getvalue()
                logging.info("Image conversion to grayscale done")

                # Send grayscale image to sync server
                scaled_image_data = await send_to_sync_server(grayscale_image_data)

                # Send scaled image back to client
                writer.write(scaled_image_data)
                await writer.drain()
            except Exception as e:
                logging.error(f"Error processing image: {e}")
            finally:
                writer.close()
                logging.info("Connection closed")
            break

async def start_async_server(ip, port):
    server = await asyncio.start_server(handle_client, ip, port)
    logging.info(f"Async server started on {ip}:{port}")
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(start_async_server('127.0.0.1', 8000))