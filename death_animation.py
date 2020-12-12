import sys
from math import ceil
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def is_empty(states, i, j, k):
    return states[i,j,k,3] == 0

def fall(states, new_states, i, j, k, di):
    if i + di < new_states.shape[0]:
        neighbors = [
            (j - 1 >= 0, (i + di, j - 1, k)),
            (j + 1 < new_states.shape[1], (i + di, j + 1, k)),
            (k - 1 >= 0, (i + di, j, k - 1)),
            (k + 1 < new_states.shape[2], (i + di, j, k + 1)),
        ]
        np.random.shuffle(neighbors)
        if is_empty(new_states, i + di, j, k):
            new_states[i+di,j,k] = states[i,j,k]
            return True
        elif neighbors[0][0] and is_empty(new_states, *neighbors[0][1]):
            x, y, z = neighbors[0][1]
            new_states[x,y,z] = states[i,j,k]
            return True
        elif neighbors[1][0] and is_empty(new_states, *neighbors[1][1]):
            x, y, z = neighbors[1][1]
            new_states[x,y,z] = states[i,j,k]
            return True
        elif neighbors[2][0] and is_empty(new_states, *neighbors[2][1]):
            x, y, z = neighbors[2][1]
            new_states[x,y,z] = states[i,j,k]
            return True
        elif neighbors[3][0] and is_empty(new_states, *neighbors[3][1]):
            x, y, z = neighbors[3][1]
            new_states[x,y,z] = states[i,j,k]
            return True
        else:
            return False
    else:
        return False

def step(states, di_max):
    new_states = np.zeros(states.shape, dtype=np.uint8)
    for i in reversed(range(states.shape[0])):
        for j in range(states.shape[1]):
            for k in range(states.shape[2]):
                if not is_empty(states, i, j, k):
                    assert(states[i,j,k,3] == 255)
                    placed = False
                    for di in reversed(range(1, np.random.randint(2, di_max + 2))):
                        placed = fall(states, new_states, i, j, k, di)
                        if placed:
                            break
                    if not placed:
                        new_states[i,j,k] = states[i,j,k]
    return new_states

def project(states):
    image = np.zeros((states.shape[0], states.shape[1], states.shape[3]), dtype=np.uint8)
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            for k in range(states.shape[2]):
                if not is_empty(states, i, j, k):
                    image[i,j] = states[i,j,k]
                    break
    return Image.fromarray(image, mode='RGBA')

def save_image(image, image_path, i):
    path = image_path[:image_path.rfind('.')] + '_death_{}.png'.format(i)
    image.save(path, compress_level=9)

if __name__ == '__main__':
    # Read arguments
    if len(sys.argv) < 5:
        print('Too few arguments')
        exit()
    image_path = sys.argv[1]
    nb_images = int(sys.argv[2])
    depth = int(sys.argv[3])
    di_max = int(sys.argv[4])
    if len(sys.argv) > 5:
        print(int(sys.argv[5]))
        np.random.seed(int(sys.argv[5]))
    # Initialize the cellular automaton
    image = np.asarray(Image.open(image_path).convert('RGBA'))
    states = np.zeros((image.shape[0], image.shape[1], depth, image.shape[2]), dtype=np.uint8)
    states[:,:,depth//2] = image
    # Run the cellular automaton to generate frames
    images = []
    i = 0
    while True:
        print(i)
        new_states = step(states, di_max)
        if (new_states == states).all():
            break
        else:
            states = new_states
            images.append(project(states))
        i += 1
    # Skipping frames
    images = [images[(i * (len(images) - 1)) // (nb_images - 1)] for i in range(nb_images)]
    animation = np.zeros((image.shape[0], image.shape[1] * nb_images, 4), dtype=np.uint8)
    # Save frames
    for i, frame in enumerate(images):
        save_image(frame, image_path, i)
        animation[:image.shape[0],i*image.shape[1]:(i+1)*image.shape[1],:] = np.asarray(frame)
    save_image(Image.fromarray(animation, mode='RGBA'), image_path, 'animation')
    # Set transparent pixels to white
    for i, frame in enumerate(images):
        new_frame = Image.new("RGBA", frame.size, "WHITE")
        new_frame.paste(frame, (0, 0), frame) 
        images[i] = new_frame
    # Generate gif
    images[0].save("demo.gif", save_all=True, append_images=images[1:], duration=125, loop=0)