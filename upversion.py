#!/bin/env python
# -*- coding: utf-8 -*-

import re
import click
from versio.version import Version


VERSION_RE = r"""
(?P<name>\s*{name}\s*=\s*)  # NAME =
([urb]?["'])                # u'
(?P<version>[^"']+)         # VERSION
(["'])                      # '
"""


def error(message, *args, **kwargs):
    raise click.ClickException(message.format(*args, **kwargs))


def compile_re(var):
    return re.compile(VERSION_RE.format(name=var), re.VERBOSE)


def extract_version(path, var):
    """Parse version from file

    :path: Path to the version file
    :var: var name to which is assigned
    """
    with open(path) as stream:
        content = stream.read()

    match = compile_re(var).search(content)
    if match is None:
        error(u'Could not find \'{} = "x.x.x"\' in file "{}"', var, path)

    return match.group('version')


def write_version(path, var, version):
    r = compile_re(var)

    with open(path, 'r') as stream:
        content = stream.read()

    with open(path, 'w') as stream:
        stream.write(r.subn(r'\g<1>\g<2>{}\g<4>'.format(version), content)[0])


@click.group()
@click.version_option()
def cli():
    """Handle version numbers"""


def options(function):
    opts = [
        click.option(u'--path', default='./setup.py', envvar=u'UPVERSION_PATH',
            show_default=True, help="Path to the file containing the version",
            type=click.Path(dir_okay=False, exists=True, resolve_path=True)),
        click.option(u'--var', default='version', envvar=u'UPVERSION_VAR',
                     show_default=True, help=u"Name of the variable to wich "
                     u"the version string is assigned"),
        click.option(u'-M', u'--major', is_flag=True,
                     help="Increase version major number M+1.m.p"),
        click.option(u'-m', u'--minor', is_flag=True,
                     help="Increase version minor number M.m+1.p"),
        click.option(u'-p', u'--patch', is_flag=True,
                     help="Increase version patch number M.m.p+1"),
        click.option(u'-d', u'--dev', is_flag=True,
                     help="Increase version dev number M.m.p.dev+1"),
        click.option(u'-P', u'--post', is_flag=True,
                     help="Increase version post number M.m.p.post+1")
    ]

    for option in opts:
        function = option(function)

    return function


def change_version(version, **flags):
    new_version = upversion(version, **flags)
    click.echo(u'From {} to {}'.format(version, new_version))
    return new_version


def upversion(version, major, minor, patch, dev, post):
    v = Version(version)

    if major:
        v.bump('major')

    if minor:
        v.bump('minor')

    if patch:
        v.bump('tiny')

    if post:
        v.bump('post')

    if dev:
        v.bump('dev')

    return str(v)


def check_number_arguments(**kwargs):
    if not any(kwargs.values()):
        options = u' '.join(u'--' + opt for opt in kwargs)
        raise click.UsageError(
            u'Should specify at least one number to increase, use ' + options)


@cli.command()
@options
def view(path, var, **flags):
    check_number_arguments(**flags)
    change_version(extract_version(path, var), **flags)


@cli.command()
@options
def up(path, var, **flags):
    check_number_arguments(**flags)
    new_version = change_version(extract_version(path, var), **flags)
    click.secho(u'writing "{}"'.format(path), fg='yellow')
    write_version(path, var, new_version)
