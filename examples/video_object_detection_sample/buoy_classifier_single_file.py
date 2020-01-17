###########################
#Author: Benoit Jeaurond  #
###########################


### Needs the graph and labels at the same directory ###

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import tensorflow as tf

import argparse

import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

MODEL_FILE = "retrained_graph.pb"
LABEL_FILE = "retrained_labels.txt"


def load_graph():
    graph = tf.Graph()
    graph_def = tf.GraphDef()

    with open(MODEL_FILE, "rb") as f:
        graph_def.ParseFromString(f.read())
    with graph.as_default():
        tf.import_graph_def(graph_def)

    return graph


def load_labels():
    label = []
    proto_as_ascii_lines = tf.gfile.GFile(LABEL_FILE).readlines()
    for l in proto_as_ascii_lines:
        label.append(l.rstrip())
    return label


def read_tensor_from_image_file(file_name, input_height=299, input_width=299, input_mean=0, input_std=255):
    input_name = "file_reader"
    output_name = "normalized"
    file_reader = tf.read_file(file_name, input_name)
    if file_name.endswith(".png"):
        image_reader = tf.image.decode_png(file_reader, channels=3, name='png_reader')
    elif file_name.endswith(".gif"):
        image_reader = tf.squeeze(tf.image.decode_gif(file_reader, name='gif_reader'))
    elif file_name.endswith(".bmp"):
        image_reader = tf.image.decode_bmp(file_reader, name='bmp_reader')
    else:
        image_reader = tf.image.decode_jpeg(file_reader, channels=3, name='jpeg_reader')
    float_caster = tf.cast(image_reader, tf.float32)
    dims_expander = tf.expand_dims(float_caster, 0);
    resized = tf.image.resize_bilinear(dims_expander, [input_height, input_width])
    normalized = tf.divide(tf.subtract(resized, [input_mean]), [input_std])
    sess = tf.Session()
    result = sess.run(normalized)

    return result


if __name__ == "__main__":

    file_name = "pic.jpg"
    input_layer = "input"
    output_layer = "final_result"
    input_height = 224
    input_width = 224
    input_mean = 128
    input_std = 128

    # Specify file name
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", help="image to be processed")
    args = parser.parse_args()

    if args.image:
        file_name = args.image

    graph = load_graph()
    labels = load_labels()
    input_name = "import/" + input_layer
    output_name = "import/" + output_layer
    input_operation = graph.get_operation_by_name(input_name)
    output_operation = graph.get_operation_by_name(output_name)

    t = read_tensor_from_image_file(file_name,
                                    input_height=input_height,
                                    input_width=input_width,
                                    input_mean=input_mean,
                                    input_std=input_std)
    frame = read_tensor_from_image_file(file_name)

    with tf.Session(graph=graph) as sess:
        results = sess.run(output_operation.outputs[0], {input_operation.outputs[0]: t})
    results = np.squeeze(results)

    top_k = results.argsort()[-5:][::-1]

    if 'buoy' == labels[top_k[0]]:
        print(True, end=" ")
    else:
        print(False, end=" ")

    # To get percentage
    # print(results[1] * 100, '%')

