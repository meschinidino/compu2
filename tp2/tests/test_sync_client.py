import socket
import struct
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def test_sync_server(image_path, scale_factor):
    with open(image_path, 'rb') as f:
        image_data = f.read()

    packed_data = struct.pack('f', scale_factor) + image_data

    try:
        logging.info("Connecting to sync server")
        with socket.create_connection(('127.0.0.1', 8888)) as sock:
            logging.info("Connected to sync server")
            sock.sendall(packed_data)
            logging.info("Data sent to sync server")
            scaled_image_data = b""
            while True:
                packet = sock.recv(4096)
                if not packet:
                    break
                scaled_image_data += packet
            logging.info("Data received from sync server")
            with open('scaled_image.jpg', 'wb') as out_file:
                out_file.write(scaled_image_data)
            logging.info("Scaled image saved as scaled_image.jpg")
    except Exception as e:
        logging.error("Error communicating with sync server: %s", e)

if __name__ == "__main__":
    test_sync_server('/home/dino/PycharmProjects/compu2/tp2/fallout.jpeg', 0.5)