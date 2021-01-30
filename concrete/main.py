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

    cmd = "python yolov3/detect.py --help"
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
