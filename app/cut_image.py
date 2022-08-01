import numpy as np
import random
from PIL import Image
import math

from .utils import reshape_split, shuffle_img_tiles, unsplit

# def cut_image(img_data, rows, cols):
#   # Prepare the image
#   cropped_img = img_data.crop((0, 0, img_data.width-(img_data.width % cols), img_data.height-(img_data.height % rows)))
#   img = np.array(cropped_img)
#   height, width, colorScheme = img.shape

#   sec_height = height // rows
#   sec_width = width // cols

#   # Break up
#   chunks= []
#   for y in range(rows):
#     for x in range(cols):
#       x_scalar = np.arange(sec_width * x, sec_width * (x + 1))
#       y_scalar = np.arange(sec_height * y, sec_height * (y + 1))
#       chunks.append(img[y_scalar[:,None], x_scalar[None,:]])

#   final_rows = []
#   for i in range(rows):
#     choices = [chunks.pop(random.randrange(len(chunks))) for i in range(cols)]
#     final_rows.append(np.hstack(choices))

#   final = np.vstack(final_rows)
#   data = Image.fromarray(np.uint8(final))
#   return data

def shuffle_img(img: Image, rows: int, cols: int):
    new_dimensions = (math.lcm(img.size[0], cols), math.lcm(img.size[1], rows))
    new_img = img.resize(new_dimensions, Image.NEAREST)
    new_img_arr = np.array(new_img)

    img_tiles = reshape_split(new_img_arr, rows, cols)
    img_tiles_shuffled = shuffle_img_tiles(img_tiles, rows, cols)
    img_unsplit = unsplit(img_tiles_shuffled)

    return Image.fromarray(img_unsplit, 'RGB').resize(img.size)
