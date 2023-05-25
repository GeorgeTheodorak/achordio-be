import io

from PIL import Image


def downscale_image(img_src: str, output_size: tuple) -> bytes:
    # Open the image file
    with open(img_src, "rb") as file:
        # Read the image as binary data
        image_data = file.read()

    # Create a PIL Image object from the binary data
    image = Image.open(io.BytesIO(image_data))

    # Downscale the image to the desired size
    image = image.resize(output_size)

    # Get the downscaled image data as bytes
    byte_stream = io.BytesIO()
    image.save(byte_stream, format='JPEG')
    image_data_downscaled = byte_stream.getvalue()

    return image_data_downscaled
