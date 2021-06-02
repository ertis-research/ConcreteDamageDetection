"""
    cli module
"""

__version__ = "0.0.1"

import os
import subprocess

import cv2
import click
from dotenv import load_dotenv

from concrete.object_detection import inference
from concrete.cli.examples import hello
from concrete.cli.utils import prepare_codebrim_yolo, split_data, data_augmentation

import torch
import numpy as np
# import neptune.alpha as neptune
from PIL import Image
from matplotlib import pyplot as plt

load_dotenv(dotenv_path=".env")


@click.group()
@click.version_option(version=__version__)
@click.option('--debug/--no-debug', default=False, help="Run the program in debug mode. [NOT IMPLEMENTED YET]")
@click.pass_context
def cli(ctx, debug):
    """
        Commands to manipulate CODEBRIM dataset.
    """    
    ctx.ensure_object(dict)

    # Define the common variable here.
    ctx.obj['DEBUG'] = debug

@cli.command()
@click.option('--image-path', type=click.Path(exists=True), help="Folder path that contains the images.", required=True)
@click.option('--annotation-path', type=click.Path(exists=True), help="Folder path that contains the annotations for each image.", required=True)
@click.option('--output', type=click.Path(), help="Output folder path that will contain the resulting text files with the bounding boxes in YOLO format.", required=True)
@click.pass_context
def prepare(ctx, image_path, annotation_path, output):
    """
        From an XML file, obtain the bounding boxes in YOLO format:

            [x_center, y_center, withd, height]

        These values are normalized.
    """
    # image_path = "datasets/CODEBRIM/original_dataset/images"
    # annotation_path = "datasets/CODEBRIM/original_dataset/annotations"
    # output = "datasets/CODEBRIM/original_dataset/labels"
    error_message = "{} Dataset path does not exist: {}"
    if not os.path.exists(image_path):
        print(error_message.format("CODEBRIM", image_path))
    elif not os.path.exists(annotation_path):
        print(error_message.format("CODEBRIM", annotation_path))
    else:
        if not os.path.exists(output):
            os.makedirs(output)
        prepare_codebrim_yolo( image_path, annotation_path, output )

@cli.command()
@click.option('--train', type=float, default=0.7, help="Fraction of the dataset used during training.", required=True)
@click.option('--val', type=float, default=0.1, help="Fraction of the dataset used in the validation set.", required=True)
@click.option('--test', type=float, default=0.2, help="Fraction of the dataset used in the test set.", required=True)
@click.option('--image-path', type=click.Path(exists=True), help="Folder path that contains the images of the dataset.", required=True)
@click.option('--label-path', type=click.Path(exists=True), help="Folder path that contains the labels or annotations of the dataset.", required=True)
@click.option('--output', type=click.Path(), help="Output folder path that will contain the different sets separated by folders.", required=True)
@click.pass_context
def split(ctx, train, val, test, image_path, label_path, output):
    """
        Split the dataset in train, val, and test set separated by folders.
    """
    # train = 0.75
    # val = 0.0
    # test = 0.25
    # label_path = "datasets/CODEBRIM/original_dataset/labels"
    # image_path = "datasets/CODEBRIM/original_dataset/images"
    # output = "datasets/CODEBRIM-75"

    error_message = "{} path does not exist: {}"
    if not os.path.exists(image_path):
        print(error_message.format("CODEBRIM", image_path))
    elif not os.path.exists(label_path):
        print(error_message.format("CODEBRIM", label_path))
    else:
        if not os.path.exists(output):
            os.makedirs(output)
        split_data( label_path, image_path, output, train, val, test )

@cli.command()
@click.option('--image-path', type=click.Path(exists=True), help="Folder path that contains the images of the dataset.", required=True)
@click.option('--label-path', type=click.Path(exists=True), help="Folder path that contains the labels or annotations of the dataset.", required=True)
@click.option('--output-images', type=click.Path(), help="Output folder path that will contain the different modified images.", required=True)
@click.option('--output-labels', type=click.Path(), help="Output folder path that will contain the different resulting bounding boxes after the image modification.", required=True)
@click.pass_context
def augment(ctx, image_path, label_path, output_images, output_labels):
    """
        Using Albumentation library pipeline to data augment.
    """
    # label_path = "datasets/CODEBRIM-DATA-AUGMENTED/original_dataset/annotations"
    # image_path = "datasets/CODEBRIM/images/train"
    # # image_path = "datasets/CODEBRIM-DATA-AUGMENTED/images/val"
    # # image_path = "datasets/CODEBRIM-DATA-AUGMENTED/images/test"
    # output_images = "datasets/CODEBRIM-DATA-AUGMENTED/original_dataset/augmented/images"
    # output_labels = "datasets/CODEBRIM-DATA-AUGMENTED/original_dataset/augmented/labels"
    data_augmentation(image_path, label_path, output_images, output_labels, 1)

if __name__ == '__main__':
    cli()