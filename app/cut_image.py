import numpy as np
import random
from PIL import Image
import math

from .utils import reshape_split, shuffle_img_tiles, unsplit, chunkify_array, random_reassemble

def cut_image(original_image: Image, rows:int, cols:int, turn: bool=False):
  # Prepare the image
  if turn: original_image.rotate(270)
  cropped_img = original_image.crop((0, 0, original_image.width-(original_image.width % cols), original_image.height-(original_image.height % rows)))
  img = np.array(cropped_img)
  height, width = img.shape[0], img.shape[1]

  sec_size = (width // cols, height // rows)

  # Process
  chunks = chunkify_array(img, rows, cols, sec_size)
  final = random_reassemble(chunks, rows, cols)

  if np.array_equal(img, final):
    return cut_image(original_image, rows, cols, turn)

  data = Image.fromarray(final)
  return data

def shuffle_img(img: Image, rows: int, cols: int, turn: bool=False):
    new_dimensions = (math.lcm(img.size[0], cols), math.lcm(img.size[1], rows))
    new_img = img.resize(new_dimensions, Image.NEAREST)

    # new_img = img.crop((0, 0, img.width-(img.width % cols), img.height-(img.height % rows)))

    new_img_arr = np.array(new_img) # change to new_img if uncommenting the resizing shizzle
    if turn:
      new_img_arr = np.rot90(new_img_arr, 3)

    img_tiles = reshape_split(new_img_arr, rows, cols)
    img_tiles_shuffled = shuffle_img_tiles(img_tiles, rows, cols)
    img_unsplit = unsplit(img_tiles_shuffled)

    return Image.fromarray(img_unsplit, 'RGB').resize(img.size)
