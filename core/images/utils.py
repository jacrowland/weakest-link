from bing_image_downloader import downloader as bing_downloader
import os
import shutil
import contextlib
from PIL import Image, ImageFilter, ImageOps
from utils import print_with_delay

ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", " "]

def _download_image(query_string, output_dir='assets/images'):
    with open(os.devnull, "w") as f, contextlib.redirect_stdout(f):
        bing_downloader.download(query_string, limit=1,  output_dir=output_dir, adult_filter_off=True, force_replace=False, timeout=60, verbose=True)
        return f"{output_dir}/{query_string}/image_1.jpg"

def _resize(image, new_width = 100):
    width, height = image.size
    ratio = height / width
    new_height = int(new_width * ratio / 2)
    return image.resize((new_width, new_height))

def _to_greyscale(image):
    return image.convert("L")

def _find_edges(image):
    return image.filter(ImageFilter.Kernel((3, 3), (-1, -1, -1, -1, 8,-1, -1, -1, -1), 1, 0))

def _invert_image(image):
    return ImageOps.invert(image)

def _pixel_to_ascii(image):
    pixels = image.getdata()
    ascii_str = ""
    for pixel in pixels:
        ascii_str += ASCII_CHARS[pixel//25];
    return ascii_str

def _format_ascii_str(image, ascii_str)->str:
    img_width = image.width
    ascii_str_len = len(ascii_str)
    ascii_img=""
    for i in range(0, ascii_str_len, img_width):
        ascii_img += ascii_str[i:i+img_width] + "\n"
    return ascii_img

def _add_border(image):
    return ImageOps.expand(image, border=0, fill=255)

def _output_ascii_to_file(ascii_img, query_string)->None:
    with open(f"assets\images\{query_string}\{query_string}.txt", "w") as f:
        f.write(ascii_img)

def _generate_ascii_image(path, query_string, output_to_file=False)->str:
    try:
        image = Image.open(path)
    except:
        print(path, "Unable to find image ")

    image = _resize(image)
    image = _to_greyscale(image)
    image = _find_edges(image)
    image = _add_border(image)

    ascii_str = _pixel_to_ascii(image)
    ascii_img = _format_ascii_str(image, ascii_str)

    if output_to_file:
        _output_ascii_to_file(ascii_img, query_string)

    return ascii_img

def get_ascii_image(query_string)->str:
    output_directory = f'assets/images/tmp'
    path = _download_image(query_string, output_dir=output_directory)
    ascii_img = _generate_ascii_image(path, query_string)
    try:
        shutil.rmtree(f'{output_directory}/{query_string}')
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))
    return ascii_img

def print_ascii_art_from_file(path, delay=0.00001):
    with open(path) as f:
        lines = f.readlines()
    print_with_delay(lines, delay=delay)

def print_ascii_art(image:str, delay=0.001):
    print_with_delay(image.split("\n"), delay=delay)

