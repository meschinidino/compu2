from PIL import Image
import io


def convert_to_grayscale(image_data):
    image = Image.open(io.BytesIO(image_data))

    grayscale_image = image.convert("L")

    output = io.BytesIO()
    grayscale_image.save(output, format="JPEG")

    grayscale_image_data = output.getvalue()

    return grayscale_image_data