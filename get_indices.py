import sys
import time
import numpy as np
from PIL import Image

def get_indices(image, palette):
    color_to_index = {}
    for i in range(palette.shape[1]):
        color_to_index[tuple(palette[0,i])] = i
    indices = np.zeros((image.shape[0], image.shape[1]), dtype=np.uint8)
    print(indices.shape, image.shape, palette.shape)
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            indices[i,j] = color_to_index[tuple(image[i,j])]
    return indices

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Too few arguments: an image and a palette are expected')
        exit()
    image_path = sys.argv[1]
    palette_path = sys.argv[2]
    start = time.time()
    image = Image.open(image_path).convert('RGBA')
    palette = Image.open(palette_path)
    indices = Image.fromarray(get_indices(np.asarray(image), np.asarray(palette)), mode='L')
    indices_path = image_path[:image_path.rfind('.')] + '_indexed.png'
    indices.save(indices_path, compress_level=9)
    print(time.time() - start)