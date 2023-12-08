import sys
import os
from PIL import Image


def pixel_energy(gray_img, p1, p2):
    return abs(gray_img.getpixel(p1) - gray_img.getpixel(p2))


def calculate_seam(gray_img, start_x):
    width, height = gray_img.size
    seam_energy = 0
    seam_path = [(start_x, 0)]

    for y in range(height - 1):
        x = seam_path[-1][0]
        energies = []

        current = (x, y)
        lower_neighbour = (x, y + 1)
        lower_left_neighbour = (x - 1, y + 1)
        lower_right_neighbour = (x + 1, y + 1)

        # Down pixel energy
        energies.append((pixel_energy(gray_img, current, lower_neighbour), x))

        # Left pixel energy
        if x > 0:
            energies.append(
                (pixel_energy(gray_img, current, lower_left_neighbour), x - 1)
            )

        # Right pixel energy
        if x < width - 1:
            energies.append(
                (pixel_energy(gray_img, current, lower_right_neighbour), x + 1)
            )

        min_energy, new_x = min(energies)

        # Add to seam path
        seam_path.append((new_x, y + 1))
        seam_energy += min_energy

    return seam_energy, seam_path


def remove_seam(img, seam_path):
    width, height = img.size
    new_img = Image.new("RGB", (width - 1, height))
    pixels = new_img.load()

    for y in range(height):
        removed_x = seam_path[y][0]
        # Copy until removed_x
        for x in range(removed_x):
            pixels[x, y] = img.getpixel((x, y))
        # Copy from removed_x + 1 until end
        for x in range(removed_x + 1, width):
            pixels[x - 1, y] = img.getpixel((x, y))

    return new_img


def carve_image(image, number_of_seams):
    for _ in range(number_of_seams):
        gray_image = image.convert("L")
        width, height = gray_image.size

        seam_energies_paths = [calculate_seam(gray_image, x) for x in range(width)]
        example = [
            (59, [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)]),
            (29, [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4)]),
            (76, [(2, 0), (2, 1), (2, 2), (2, 3), (2, 4)]),
        ]

        min_seam_energy, best_seam_path = min(
            seam_energies_paths, key=lambda item: item[0]
        )

        image = remove_seam(image, best_seam_path)

    return image


def main():
    if len(sys.argv) != 3:
        print("Usage: python3 seam_carving.py /path/to/image.png number_of_seams")
        sys.exit(1)

    image_path = sys.argv[1]
    number_of_seams = int(sys.argv[2])
    image = Image.open(image_path)

    carved_image = carve_image(image, number_of_seams)

    file_name, file_extension = os.path.splitext(image_path)
    carved_image_path = f"{file_name}_carved{file_extension}"

    carved_image.save(carved_image_path)

    print(f"\nSeam carved image saved at: {carved_image_path}")

    carved_image.show()


if __name__ == "__main__":
    main()
