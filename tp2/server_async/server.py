import asyncio
import logging
from aiohttp import web
from PIL import Image
import io
import struct

logging.basicConfig(level=logging.INFO)


async def convert_to_grayscale(image_data):
    logging.info("Starting image conversion to grayscale")
    image = Image.open(io.BytesIO(image_data))
    grayscale_image = image.convert("L")
    output = io.BytesIO()
    grayscale_image.save(output, format="JPEG")
    grayscale_image_data = output.getvalue()
    logging.info("Image conversion to grayscale done")
    return grayscale_image_data


async def communicate_with_sync_server(data, scale_factor, max_retries=5, delay=5):
    for attempt in range(1, max_retries + 1):
        try:
            reader, writer = await asyncio.open_connection('localhost', 8888)

            # Pack the scale factor with the image data
            packed_data = struct.pack('f', scale_factor) + data
            writer.write(packed_data)
            await writer.drain()
            logging.info("Data sent to sync server")

            # Wait for response with a timeout
            try:
                response = await asyncio.wait_for(reader.read(), timeout=10)
                logging.info("Received scaled image data from sync server")
                writer.close()
                await writer.wait_closed()
                return response
            except asyncio.TimeoutError:
                logging.warning(f"Timeout waiting for response from sync server, attempt {attempt}")
                writer.close()
                await writer.wait_closed()

        except (ConnectionRefusedError, OSError) as e:
            logging.warning(f"Attempt {attempt} to connect to sync server failed: {e}")
            await asyncio.sleep(delay)

    raise ConnectionRefusedError("Failed to connect to sync server after multiple attempts")


async def handle_request(request):
    logging.info("Received request to process image")
    data = await request.post()

    try:
        image_data = data['image'].file.read()
        scale_factor = float(data['scale_factor'])
        grayscale_image_data = await convert_to_grayscale(image_data)
        scaled_image_data = await communicate_with_sync_server(grayscale_image_data, scale_factor)
        logging.info("Sending scaled image to client")
        return web.Response(body=scaled_image_data, content_type='image/jpeg')
    except KeyError:
        logging.error("Missing 'image' or 'scale_factor' in request")
        return web.Response(status=400, text="Bad Request: Missing 'image' or 'scale_factor'")
    except ValueError as ve:
        logging.error(f"Invalid scale factor: {ve}")
        return web.Response(status=400, text="Bad Request: Invalid 'scale_factor'")
    except ConnectionRefusedError as ce:
        logging.error(f"Sync server connection failed: {ce}")
        return web.Response(status=500, text="Internal Server Error: Sync server unavailable")


async def start_async_server(ip, port):
    logging.info(f"Starting async server on {ip}:{port}")
    app = web.Application()
    app.add_routes([web.post('/process', handle_request)])
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host=ip, port=port)
    await site.start()
    while True:
        await asyncio.sleep(3600)


if __name__ == "__main__":
    asyncio.run(start_async_server('::', 8000))
