import numpy as np
import random
from PIL import Image

def cut_image(img_data, rows, cols):
  # Prepare the image
  cropped_img = img_data.crop((0, 0, img_data.width-(img_data.width % cols), img_data.height-(img_data.height % rows)))
  img = np.array(cropped_img)
  height, width, colorScheme = img.shape

  sec_height = height // rows
  sec_width = width // cols

  # Break up
  chunks= []
  for y in range(rows):
    for x in range(cols):
      x_scalar = np.arange(sec_width * x, sec_width * (x + 1))
      y_scalar = np.arange(sec_height * y, sec_height * (y + 1))
      chunks.append(img[y_scalar[:,None], x_scalar[None,:]])

  final_rows = []
  for i in range(rows):
    choices = [chunks.pop(random.randrange(len(chunks))) for i in range(cols)]
    final_rows.append(np.hstack(choices))

  final = np.vstack(final_rows)
  data = Image.fromarray(np.uint8(final))
  return data