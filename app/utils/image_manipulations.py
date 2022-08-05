import numpy as np
import random

def unsplit(image: np.ndarray):
    img_height, img_width, tile_height, tile_width, pix = image.shape

    image = image.swapaxes(1, 2)

    tiled_array = image.reshape(
        img_height * tile_height,
        img_width * tile_width,
        pix
    )

    return tiled_array

def shuffle_img_tiles(img_tiles: np.ndarray, rows: int, cols: int):
    img_tiles_shuffled = img_tiles.copy() # Array is read_only, so to shuffle we need a copy 

    temp = img_tiles_shuffled.reshape(
        rows * cols, 
        img_tiles.shape[2], 
        img_tiles.shape[3], 
        3
    )

    np.random.shuffle(temp)
    
    return img_tiles_shuffled

def reshape_split(image: np.ndarray, rows: int, cols: int):
    img_height, img_width, channels = image.shape

    tiled_array = image.reshape(
        rows,
        img_height // rows,
        cols,
        img_width // cols,
        channels
    )

    return tiled_array.swapaxes(1, 2)

def chunkify_array(arr: np.ndarray, rows: int, cols:int, sec_size: tuple[int, int]):
  chunks= []
  for y in range(rows):
    for x in range(cols):
      x_scalar = np.arange(sec_size[0] * x, sec_size[0] * (x + 1))
      y_scalar = np.arange(sec_size[1] * y, sec_size[1] * (y + 1))
      chunks.append(arr[y_scalar[:,None], x_scalar[None,:]])
  
  return chunks

def random_reassemble(original_chunks, rows:int, cols:int):
  chunks = original_chunks.copy()
  final_rows = []
  for i in range(rows):
    choices = [chunks.pop(random.randrange(len(chunks))) for i in range(cols)]
    final_rows.append(np.hstack(choices))

  return np.vstack(final_rows)

def rebuild(original_chunks):
  chunks = original_chunks.copy()

  return np.vstack([np.hstack(row) for row in chunks])