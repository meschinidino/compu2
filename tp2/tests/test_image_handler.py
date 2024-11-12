import socket
import pytest
import io
from PIL import Image
from multiprocessing import Process
from server_sync.server import start_sync_server


@pytest.fixture(scope="module")
def sync_server():
    # Start the sync server in a separate process
    process = Process(target=start_sync_server)
    process.start()
    yield
    process.terminate()
    process.join()


def test_image_request_handler(sync_server):
    # Create a dummy image
    image = Image.new('RGB', (100, 100), color='blue')
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG")
    image_data = buffer.getvalue()

    # Connect to the sync server and send the image
    with socket.create_connection(('127.0.0.1', 8888)) as client_socket:
        client_socket.sendall(image_data)

        # Receive the scaled image data from the server
        received_data = b""
        while True:
            packet = client_socket.recv(4096)
            if not packet:
                break
            received_data += packet

    # Open the scaled image and verify its properties
    scaled_image = Image.open(io.BytesIO(received_data))
    assert scaled_image.size == (50, 50)
