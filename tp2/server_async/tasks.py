import asyncio
import logging
from PIL import Image
import io
import socket

logging.basicConfig(level=logging.INFO)

async def process_image(image_data):
    logging.info("Starting image processing")
    loop = asyncio.get_event_loop()
    image = await loop.run_in_executor(None, Image.open, io.BytesIO(image_data))
    grayscale_image = await loop.run_in_executor(None, image.convert, 'L')
    output = io.BytesIO()
    await loop.run_in_executor(None, grayscale_image.save, output, 'JPEG')
    logging.info("Finished image processing")
    return output.getvalue()

async def communicate_with_sync_server(image_data):
    logging.info("Starting communication with sync server")
    reader, writer = await asyncio.open_connection('127.0.0.1', 8888)
    writer.write(image_data)
    await writer.drain()

    data = await reader.read()
    writer.close()
    await writer.wait_closed()
    logging.info("Finished communication with sync server")
    return data