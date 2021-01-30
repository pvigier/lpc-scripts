import sys
import time
import numpy as np
from PIL import Image

def color_image(indices, palette):
    print(indices.shape, palette.shape)
    return Image.fromarray(palette[0,indices], mode='RGBA')

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Too few arguments: a greyscale image and a palette are expected')
        exit()
    indices_path = sys.argv[1]
    palette_path = sys.argv[2]
    start = time.time()
    indices = Image.open(indices_path)
    palette = Image.open(palette_path)
    image = color_image(np.asarray(indices), np.asarray(palette))
    image_path = indices_path[indices_path.rfind('/')+1:indices_path.rfind('.')] + '_colored.png'
    image.save(image_path, compress_level=9)
    print(time.time() - start)