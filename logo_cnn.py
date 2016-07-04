#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import tensorflow as tf
import numpy as np
import os

FLAGS = tf.app.flags.FLAGS

tf.app.flags.DEFINE_string(
    "train_dir", "flickr_logos_27_dataset",
    "Directory where to write event logs and checkpoint.")
tf.app.flags.DEFINE_integer("max_steps", 10000, "Number of batches to run.")
tf.app.flags.DEFINE_integer("image_size", 64, "Size of an input image.")


def read_flickrlogos27(filename_queue):
    class FlickrLogos27Record():
        pass

    result = FlickrLogos27Record()

    label_bytes = 1
    result.width = 32
    result.height = 32
    result.depth = 3
    image_bytes = result.width * result.height * result.depth
    record_bytes = label_bytes + image_bytes

    reader = tf.FixedLengthRecordReader(record_bytes=record_bytes)


def cropped_inputs():
    if tf.gfile.Exists(os.path.join(
            FLAGS.train_dir,
            'flickr_logos_27_dataset_training_set_annotation.txt')):
        raise ValueError(
            'Failed to find file: flickr_logos_27_dataset_training_set_annotation.txt')
    annot_train = np.loadtxt(
        os.path.join(FLAGS.train_dir,
                     'flickr_logos_27_dataset_training_set_annotation.txt'))

    filenames = [os.path.join(FLAGS.train_dir, annot[0])
                 for annot in annot_train]

    filename_queue = tf.train.input_producer(filenames)

    read_input = read_flickrlogos27(filename_queue)


def convolutional_layer():
    x = tf.placeholder(tf.float32, [None, None, None])

    w_conv1 = tf.Variable(tf.truncated_normal([5, 5, 1, 48], stddev=0.1))
    b_conv1 = tf.Variable(tf.constant([48]))
    x_expanded = tf.expand_dims(x, 3)
    conv1 = tf.nn.conv2d(x_expanded, w_conv1, strides=(1, 1), padding='SAME')
    h_conv1 = tf.nn.relu(conv1 + b_conv1)
    h_pool1 = tf.nn.max_pool(h_conv1,
                             ksize=[1, 2, 2, 1],
                             stride=[1, 2, 2, 1],
                             padding='SAME')


def inference():
    x, conv_layer, conv_vars = convolutional_layer()


def train():
    with tf.Graph().as_default():
        images, labels = cropped_inputs()

        logits = inference()


def main():
    if not tf.gfile.Exists(FLAGS.train_dir):
        print("Not found: %s" % (FLAGS.train_dir))
    train()


if __name__ == '__main__':
    main()
