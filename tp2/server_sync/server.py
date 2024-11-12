import socketserver
import logging
from tp2.server_sync.image_processing import scale_image
import struct

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class ImageRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        try:
            logging.info("Handling new request from %s", self.client_address)
            data = b""
            while True:
                packet = self.request.recv(4096)
                if not packet:
                    break
                data += packet
            logging.info("Data received from client: %d bytes", len(data))

            if len(data) < 4:
                logging.error("Received data is too short to contain a scale factor")
                return

            # Extract scale factor and image data
            scale_factor = struct.unpack('f', data[:4])[0]
            image_data = data[4:]
            logging.info("Extracted scale factor: %f", scale_factor)

            if not image_data:
                logging.error("No image data received after scale factor")
                return

            # Process the image
            scaled_image = scale_image(image_data, scale_factor)
            logging.info("Image scaling complete")

            # Send scaled image back to client
            self.request.sendall(scaled_image)
            logging.info("Scaled image sent to client")

        except Exception as e:
            logging.error("Error in processing request: %s", e)

def start_sync_server():
    try:
        with socketserver.ThreadingTCPServer(('0.0.0.0', 8888), ImageRequestHandler) as server:
            logging.info("Sync server running on port 8888")
            server.serve_forever()
    except OSError as e:
        if e.errno == 98:
            logging.error("Port 8888 is already in use")
        else:
            raise

if __name__ == "__main__":
    start_sync_server()
