#!/bin/python
# Python 2.7.x script to generate fractal images
# Run fractal.py for usage

from PIL import Image
import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import math
import sys

usage = """
fractal.py [julia | mandelbrot]
    --size  <width>x<height> : specify size of image (default 1920x1080)
    --shift <real> <imag>    : shift the origin by this number (default 0+0j)
    --zoom  <zoom_value>     : zoom amount into image (default 1)
    --const <real> <imag>    : constant used for the quadratic function (default (phi-2)+(phi-1)j)
    --cmap  <cmap_name>      : color palette name (default viridis)
"""

def create_cmap(colour_strings):
    colour_strings = [colour.lower() for colour in colour_strings]
    cmap_name = '_'.join(colour_strings)
    colour_list = []
    for colour in colour_strings:
        try:
            colour_tuple = (int(colour[0:2], 16)/256.0, int(colour[2:4], 16)/256.0, int(colour[4:-1], 16)/256.0)
            colour_list.append(colour_tuple)
        except:
            print 'Error - Invalid colour hex values.'
            sys.exit(1)
            
    return LinearSegmentedColormap.from_list(cmap_name, colour_list, N=1024)

def create_fractal(width, height, c, shift=complex(0, 0), zoom=1, cmap_name='viridis', maxiter=256):
    R = maxiter*abs(c)
    Rsq = R**2

    short_side = min(width,height)
    scale = 2.0/(zoom*(short_side - 1))

    plt_cmaps = ['Accent', 'Accent_r', 'Blues', 'Blues_r', 'BrBG', 'BrBG_r', 'BuGn', 'BuGn_r', 'BuPu', 'BuPu_r', 'CMRmap', 'CMRmap_r', 'Dark2', 'Dark2_r', 'GnBu', 'GnBu_r', 'Greens', 'Greens_r', 'Greys', 'Greys_r', 'OrRd', 'OrRd_r', 'Oranges', 'Oranges_r', 'PRGn', 'PRGn_r', 'Paired', 'Paired_r', 'Pastel1', 'Pastel1_r', 'Pastel2', 'Pastel2_r', 'PiYG', 'PiYG_r', 'PuBu', 'PuBuGn', 'PuBuGn_r', 'PuBu_r', 'PuOr', 'PuOr_r', 'PuRd', 'PuRd_r', 'Purples', 'Purples_r', 'RdBu', 'RdBu_r', 'RdGy', 'RdGy_r', 'RdPu', 'RdPu_r', 'RdYlBu', 'RdYlBu_r', 'RdYlGn', 'RdYlGn_r', 'Reds', 'Reds_r', 'Set1', 'Set1_r', 'Set2', 'Set2_r', 'Set3', 'Set3_r', 'Spectral', 'Spectral_r', 'Wistia', 'Wistia_r', 'YlGn', 'YlGnBu', 'YlGnBu_r', 'YlGn_r', 'YlOrBr', 'YlOrBr_r', 'YlOrRd', 'YlOrRd_r', 'afmhot', 'afmhot_r', 'autumn', 'autumn_r', 'binary', 'binary_r', 'bone', 'bone_r', 'brg', 'brg_r', 'bwr', 'bwr_r', 'cividis', 'cividis_r', 'cool', 'cool_r', 'coolwarm', 'coolwarm_r', 'copper', 'copper_r', 'cubehelix', 'cubehelix_r', 'flag', 'flag_r', 'gist_earth', 'gist_earth_r', 'gist_gray', 'gist_gray_r', 'gist_heat', 'gist_heat_r', 'gist_ncar', 'gist_ncar_r', 'gist_rainbow', 'gist_rainbow_r', 'gist_stern', 'gist_stern_r', 'gist_yarg', 'gist_yarg_r', 'gnuplot', 'gnuplot2', 'gnuplot2_r', 'gnuplot_r', 'gray', 'gray_r', 'hot', 'hot_r', 'hsv', 'hsv_r', 'inferno', 'inferno_r', 'jet', 'jet_r', 'magma', 'magma_r', 'nipy_spectral', 'nipy_spectral_r', 'ocean', 'ocean_r', 'pink', 'pink_r', 'plasma', 'plasma_r', 'prism', 'prism_r', 'rainbow', 'rainbow_r', 'seismic', 'seismic_r', 'spring', 'spring_r', 'summer', 'summer_r', 'tab10', 'tab10_r', 'tab20', 'tab20_r', 'tab20b', 'tab20b_r', 'tab20c', 'tab20c_r', 'terrain', 'terrain_r', 'viridis', 'viridis_r', 'winter', 'winter_r']

    if cmap_name in plt_cmaps:
        cmap = plt.get_cmap(cmap_name,lut=256)
    else:
        cmap = create_cmap(list(cmap_name.split('_')))
    impala = [int(math.floor(cmap(val/256.0)[index]*255)) for val in range(256) for index in range(3)]
    img = Image.new('P', (width, height))
    img.putpalette(impala)
    pixels = img.load()

    for x in range(width):
        for y in range(height):
            z = complex((x - width/2)*scale - shift.real, (-y + height/2)*scale - shift.imag)

            value = 0
            while abs(z)**2 < Rsq and value < maxiter:
                z = z*z + c
                value = value + 1

            pixels[x,y] = value % maxiter

    return img

def main():
    if len(sys.argv) < 2:
        print usage
        sys.exit(1)

    fractype = sys.argv[1]

    if '--size' in sys.argv:
        arg_index = sys.argv.index('--size') + 1
        width, height = [int(num) for num in sys.argv[arg_index].split('x')]
    else:
        width, height = 1920, 1080

    if '--shift' in sys.argv:
        arg_index = sys.argv.index('--shift') + 1
        shift = complex(float(sys.argv[arg_index]), float(sys.argv[arg_index + 1]))
    else:
        shift = complex(0,0)

    if '--zoom' in sys.argv:
        arg_index = sys.argv.index('--zoom') + 1
        zoom = float(sys.argv[arg_index])
    else:
        zoom = 1

    if '--const' in sys.argv:
        arg_index = sys.argv.index('--const') + 1
        c = complex(float(sys.argv[arg_index]), float(sys.argv[arg_index + 1]))
    else:
        c = complex(-0.3819, 0.6180)

    if '--cmap' in sys.argv:
        arg_index = sys.argv.index('--cmap') + 1
        cmap_name = sys.argv[arg_index]
    else:
        cmap_name = 'viridis'

    img = create_fractal(width=width, height=height, c=c,shift=shift, zoom=zoom, cmap_name=cmap_name)
    img.save(fractype + '_' + str(c.real) + '_i' + str(c.imag) + '.png')

if __name__ == '__main__':
    main()
