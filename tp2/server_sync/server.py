import socketserver
from multiprocessing import Process
from PIL import Image
import io


def resize_image(data, scale_factor=0.5):
    image = Image.open(io.BytesIO(data))
    width, height = image.size
    resized_image = image.resize((int(width * scale_factor), int(height * scale_factor)))
    output = io.BytesIO()
    resized_image.save(output, format='JPEG')
    output.seek(0)
    return output.read()

class ImageRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(10000)
        resized_image_data = resize_image(data)
        self.request.sendall(resized_image_data)

def start_sync_server():
    process = Process(target=run_sync_server)
    process.start()

def run_sync_server():
    with socketserver.TCPServer(('localhost', 8888), ImageRequestHandler) as server:
        print("Sync server started on localhost:8888")
        server.serve_forever()