import cv2
import os
import logging

import numpy as np
from imageio import imread
import matplotlib
from matplotlib import pyplot as plt

import morphsnakes as ms

# in case you are running on machine without display, e.g. server
if os.environ.get('DISPLAY', '') == '':
    logging.warning('No display found. Using non-interactive Agg backend.')
    matplotlib.use('Agg')

PATH_IMG_LIVERS = 'images/pic0032.png'


def visual_callback_2d(background, fig=None):

    # Prepare the visual environment.
    if fig is None:
        fig = plt.figure()
    fig.clf()
    ax1 = fig.add_subplot(1, 2, 1)
    ax1.imshow(background, cmap=plt.cm.gray)

    ax2 = fig.add_subplot(1, 2, 2)
    ax_u = ax2.imshow(np.zeros_like(background), vmin=0, vmax=1)
    plt.pause(0.001)

    def callback(levelset):

        if ax1.collections:
            del ax1.collections[0]
        ax1.contour(levelset, [0.5], colors='r')
        ax_u.set_data(levelset)
        fig.canvas.draw()
        plt.pause(0.001)

    return callback


def rgb2gray(img):
    """Convert a RGB image to gray scale."""
    return 0.2989 * img[..., 0] + 0.587 * img[..., 1] + 0.114 * img[..., 2]



def example_livers():
    logging.info('Running: example_nodule (MorphGAC)...')

    # Load the image.
    img = imread(PATH_IMG_LIVERS)[..., 0] / 255.0

    # g(I)
    # gimg = ms.inverse_gaussian_gradient(img, alpha=1000, sigma=5.48)
    gimg = ms.inverse_gaussian_gradient(img, alpha=1500, sigma=6.7)

    # Initialization of the level-set.
    init_ls = ms.circle_level_set(img.shape, (120, 150), 17)

    # Callback for visual plotting
    callback = visual_callback_2d(img)

    # MorphGAC.
    ms.morphological_geodesic_active_contour(gimg, iterations=1200,
                                             init_level_set=init_ls,
                                             smoothing=1, threshold=0.42,
                                             balloon=1, iter_callback=callback)
    
    

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    example_livers()

    # Uncomment the following line to see a 3D example
    # This is skipped by default since mplot3d is VERY slow plotting 3d meshes
    # example_confocal3d()

    logging.info("Done.")
    plt.show()