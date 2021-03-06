from __future__ import print_function
import os
import sys

import click
from galaxy.tools.deps import commands
from galaxy.tools.deps.commands import which


def shell(cmds, **kwds):
    info(cmds)
    return commands.shell(cmds, **kwds)


def info(message, *args):
    if args:
        message = message % args
    _echo(click.style(message, bold=True, fg='green'))


def can_write_to_path(path, **kwds):
    if not kwds["force"] and os.path.exists(path):
        error("%s already exists, exiting." % path)
        return False
    return True


def error(message, *args):
    if args:
        message = message % args
    _echo(click.style(message, bold=True, fg='red'), err=True)


def warn(message, *args):
    if args:
        message = message % args
    _echo(click.style(message, fg='red'), err=True)


def _echo(message, err=False):
    if sys.version_info[0] == 2:
        click.echo(message, err=err)
    else:
        print(message)


def untar_to(url, path, tar_args):
    if which("wget"):
        download_cmd = "wget -q --recursive -O - '%s'"
    else:
        download_cmd = "curl '%s'"
    download_cmd = download_cmd % url
    if tar_args:
        if not os.path.exists(path):
            os.makedirs(path)

        untar_cmd = "tar %s" % tar_args
        shell("%s | %s" % (download_cmd, untar_cmd))
    else:
        shell("%s > '%s'" % (download_cmd, path))
