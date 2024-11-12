from PIL import Image
import io

def scale_image(image_data, scale_factor):
    image = Image.open(io.BytesIO(image_data))
    new_size = (int(image.width * scale_factor), int(image.height * scale_factor))
    scaled_image = image.resize(new_size, Image.Resampling.LANCZOS)
    output = io.BytesIO()
    scaled_image.save(output, format="JPEG")
    return output.getvalue()