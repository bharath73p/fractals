#!/bin/python
# Python 2.7.x script to generate fractal images
# Run fractal.py for usage

from PIL import Image
import numpy as np
import os
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import math
import sys
import fractal as fr


def main():
    mode = 0o744
    parent_dir = './'
    dir_name = 'fracpix'
    dir_path = os.path.join(parent_dir, dir_name)
    os.mkdir(dir_path, mode)
    print 'Created dir - ' + dir_name

    zoom_val = 0.01
    
    for num in range(3600):
        zoom_val += 0.277775 
        img = fr.create_fractal(width=1080, height=1920, c=complex(0.285,0.01), shift=complex(-0.4775162185, -0.1897497681), zoom=zoom_val, cmap_name='GnBu', maxiter=256)
        img.save(dir_name + '/pic{:05d}.png'.format(num))
    print 'Done saving ' + str(num) + 'images'

if __name__ == '__main__':
    main()
