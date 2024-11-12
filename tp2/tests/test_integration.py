import asyncio
import aiohttp
import pytest
from multiprocessing import Process
from server_sync.server import start_sync_server
from server_async.server import start_async_server
from PIL import Image
import io

@pytest.fixture(scope="module")
def sync_server():
    process = Process(target=start_sync_server)
    process.start()
    yield
    process.terminate()

@pytest.fixture(scope="module")
def async_server():
    process = Process(target=start_async_server, args=('127.0.0.1', 8080))
    process.start()
    yield
    process.terminate()

@pytest.mark.asyncio
async def test_image_processing_integration(sync_server, async_server):
    async with aiohttp.ClientSession() as session:
        # Upload image for processing
        with open('/home/dino/PycharmProjects/compu2/tp2/fallout.jpeg', 'rb') as f:
            image_data = f.read()
        async with session.post('http://127.0.0.1:8080/process', data={'image': image_data}) as resp:
            assert resp.status == 200
            response_data = await resp.json()
            task_id = response_data['task_id']

        # Check task status
        while True:
            async with session.get(f'http://127.0.0.1:8080/status/{task_id}') as resp:
                if resp.status == 200:
                    processed_image = await resp.read()
                    break
                elif resp.status == 202:
                    await asyncio.sleep(1)
                else:
                    assert False, "Unexpected status code"

        # Verify processed image
        processed_image = Image.open(io.BytesIO(processed_image))
        assert processed_image.mode == 'L'