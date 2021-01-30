"""
    cli module
"""

__version__ = "0.0.1"

import os
import subprocess

import click
from dotenv import load_dotenv
from ..models.yolov3.detect import detect
# from yolov3.train import train

from object_detection import inference, train
from cli.examples import hello

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

    cmd = "python models/YOLOv3/detect.py --help"
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    out, err = p.communicate()
    click.echo(out)


@cli.command()
@click.pass_context
def desync(ctx):
    """
        Desync
    """
    click.echo('Debug is not %s' % (ctx.obj['DEBUG'] and 'off' or 'on'))
    x = inference.inference()
    click.echo(x)
    click.echo(os.getenv('TEST'))
    click.echo( hello() )
    detect()
    # train()
