import io
from PIL import Image
from server_sync.image_processing import scale_image

def test_scale_image():
    # Create a dummy image in memory
    image = Image.new('RGB', (100, 100), color='red')
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG")
    image_data = buffer.getvalue()

    # Scale the image by 0.5
    scaled_image_data = scale_image(image_data, 0.5)
    scaled_image = Image.open(io.BytesIO(scaled_image_data))

    # Verify that the scaled image has the expected size
    assert scaled_image.size == (50, 50)
