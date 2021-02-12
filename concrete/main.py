"""
    cli module
"""

__version__ = "0.0.1"

import os
import subprocess

import click
from dotenv import load_dotenv

from concrete.object_detection import inference
from concrete.cli.examples import hello

import torch
import numpy as np
import neptune.alpha as neptune
from PIL import Image
from matplotlib import pyplot as plt

load_dotenv(dotenv_path=".env")


@click.group()
@click.version_option(version=__version__)
@click.option('--debug/--no-debug', default=False)
@click.pass_context
def cli(ctx, debug):
    """
        H
    """
    ctx.ensure_object(dict)

    ctx.obj['DEBUG'] = debug


@cli.command()
@click.pass_context
def sync(ctx):
    """
        Sync
    """
    click.echo('Debug is %s' % (ctx.obj['DEBUG'] and 'on' or 'off'))

    cmd = "python yolov3/detect.py --source datasets --device 0 --save-txt"
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    out, err = p.communicate()
    click.echo(out)


@cli.command()
@click.pass_context
def desync(ctx):
    """
        Desync
    """
    # click.echo('Debug is not %s' % (ctx.obj['DEBUG'] and 'off' or 'on'))
    # x = inference.inference()
    # click.echo(x)
    # click.echo(os.getenv('TEST'))
    # click.echo( hello() )

    # api_token = os.getenv("NEPTUNE_API_TOKEN")
    # print( api_token )
    # if api_token is not None:
    #     exp = neptune.init( project="drtorresruiz/alpha", api_token=api_token )
    model = torch.hub.load( 'ultralytics/yolov3', 'yolov3', pretrained=True )
    # Images
    img = Image.open('datasets/download.jpg')
    imgs = [img]
    # Inference
    prediction = model( imgs, size=640 )
    prediction.save()
    