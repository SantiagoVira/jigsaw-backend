import numpy as np
import random
from PIL import Image
import math

from .utils import chunkify_array, rebuild

def layout_to_chunks(layout, chunks):
  return Image.fromarray(
    rebuild(
      [[chunks[idx] for idx in row] for row in layout]
      ))


def to_gif(original_image: Image, rows:int, cols:int, turn: bool=False):
  if turn: original_image.rotate(270)
  cropped_img = original_image.crop((0, 0, original_image.width-(original_image.width % cols), original_image.height-(original_image.height % rows)))
  img = np.array(cropped_img)

  height, width = img.shape[0], img.shape[1]

  sec_size = (width // cols, height // rows)

  # Break up
  chunks = chunkify_array(img, rows, cols, sec_size)

  animation_layout = np.arange(rows * cols)
  np.random.default_rng().shuffle(animation_layout)
  animation_layout = animation_layout.reshape((rows, cols))

  frames = [layout_to_chunks(animation_layout, chunks)]

  for i in range(rows*cols):
    location = list(zip(*np.where(animation_layout == i)))[0] #(row, col)
    final_location = (i // cols, i % cols)
    if location != final_location:  # Not yet in correct spot
      animation_layout[location] = animation_layout[final_location]
      animation_layout[final_location] = i
      frames.append(layout_to_chunks(animation_layout, chunks))
  
  return frames