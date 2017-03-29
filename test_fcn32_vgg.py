#!/usr/bin/env python

import os
import scipy as scp
import scipy.misc
import sys

import numpy as np
import tensorflow as tf
import argparse

import fcn32_vgg
import utils

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
CAT_DIR = os.path.join(BASE_DIR, "test_data/tabby_cat.png")

parser = argparse.ArgumentParser()
parser.add_argument("--input", type=str, default=CAT_DIR, help="path to Input file to use")
FLAGS = parser.parse_args()
FILE_DIR = FLAGS.input

from tensorflow.python.framework import ops

img1 = scp.misc.imread(FILE_DIR)

with tf.Session() as sess:
    images = tf.placeholder("float")
    feed_dict = {images: img1}
    batch_images = tf.expand_dims(images, 0)

    vgg_fcn = fcn32_vgg.FCN32VGG()
    with tf.name_scope("content_vgg"):
        vgg_fcn.build(batch_images, debug=True)

    print('Finished building Network.')

    init = tf.global_variables_initializer()
    sess.run(init)

    print('Running the Network')
    tensors = [vgg_fcn.pred, vgg_fcn.pred_up]
    down, up = sess.run(tensors, feed_dict=feed_dict)

    down_color = utils.color_image(down[0])
    up_color = utils.color_image(up[0])

    scp.misc.imsave('fcn32_downsampled.png', down_color)
    scp.misc.imsave('fcn32_upsampled.png', up_color)
