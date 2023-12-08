# Short PIL demo

from PIL import Image

image_path = "lake.png"

image = Image.open(image_path)

print(f"Format: {image.format}")
print(f"Size: {image.size}")
print(f"Mode: {image.mode}")
print(dir(image))

x, y = 10, 10
original_pixel_value = image.getpixel((x, y))
print(f"The original pixel value at position ({x}, {y}) is: {original_pixel_value}")

new_pixel_value = (255, 0, 0)
image.putpixel((x, y), new_pixel_value)
print(f"The pixel value at position ({x}, {y}) has been changed to: {new_pixel_value}")

image.save("modified_pixel.png")
