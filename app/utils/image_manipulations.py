import numpy as np

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
