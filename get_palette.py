import io
import os
import sys
import time
import numpy as np
from PIL import Image
from get_indices import get_indices

palette_size = 32

def convert_to_indexed_image(image, reduce_palette=False):
    # Print some info about the image
    print(np.asarray(image).shape)
    colors = image.getcolors()
    colors = list(reversed(sorted(colors)))
    print('Colors:')
    for x in colors:
        print(x)
    print('Number of colors:', len(colors))
    if reduce_palette:
        # Convert to an indexed image
        indexed_image = image.convert('RGBA').convert(mode='P', dither='NONE', colors=palette_size) # Be careful it can remove colors
        # Save and load the image to update the info (transparency field in particular)
        f = io.BytesIO()
        indexed_image.save(f, 'png')
        indexed_image = Image.open(f)
        indices = np.asarray(indexed_image)
        # Create the palette
        palette = indexed_image.getpalette()
        transparency = list(indexed_image.info['transparency'])
        palette_colors = np.asarray([[palette[3*i:3*i+3] + [transparency[i]] for i in range(palette_size)]], dtype=np.uint8)
        # Display the new palette
        print('Palette:')
        for x in palette_colors[0]:
            print(x)
    else:
        palette_colors = np.zeros((1, palette_size, 4), dtype=np.uint8)
        palette_colors[0,:len(colors)] = [color for n, color in colors]
        indices = get_indices(np.asarray(image), palette_colors)
    # Create the images
    indices_image = Image.fromarray(indices, 'L')
    palette_image = Image.fromarray(palette_colors, mode='RGBA')
    return indices_image, palette_image

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Too few arguments: a path is expected')
        exit()
    path = sys.argv[1]
    reduce_palette = len(sys.argv) >= 3 and sys.argv[2] == 'reduce'
    start = time.time()
    image = Image.open(path)
    indices_image, palette_image = convert_to_indexed_image(image, reduce_palette)
    path = path[:path.rfind('.')]
    indices_image.save(path + '_indices.png', compress_level=9)
    palette_image.save(path + '_palette.png', compress_level=9)
    print(time.time() - start)