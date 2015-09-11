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
def cli():
    """Handle version numbers"""


def options(function):
    opts = [
        click.option(u'--path', default='./setup.py', envvar=u'UPVERSION_PATH',
            type=click.Path(dir_okay=False, exists=True, resolve_path=True)),
        click.option(u'--var', default='version', envvar=u'UPVERSION_VAR'),
        click.option(u'-M', u'--major', is_flag=True),
        click.option(u'-m', u'--minor', is_flag=True),
        click.option(u'-p', u'--patch', is_flag=True)
    ]

    for option in opts:
        function = option(function)

    return function


def change_version(version, major, minor, patch):
    new_version = upversion(version, major, minor, patch)
    click.echo(u'From {} to {}'.format(version, new_version))
    return new_version


def upversion(version, major, minor, patch):
    v = Version(version)

    if major:
        v.bump('major')

    if minor:
        v.bump('minor')

    if patch:
        v.bump('tiny')

    return str(v)


def check_number_arguments(major, minor, patch):
    if not (major or minor or patch):
        raise click.UsageError(
            u'Should specify at least one number to increase '
            u'use --major --minor --patch')


@cli.command()
@options
def view(path, var, major, minor, patch):
    check_number_arguments(major, minor, patch)
    change_version(extract_version(path, var), major, minor, patch)


@cli.command()
@options
def up(path, var, major, minor, patch):
    check_number_arguments(major, minor, patch)
    new_version = change_version(extract_version(path, var), major, minor, patch)
    click.secho(u'writing "{}"'.format(path), fg='yellow')
    write_version(path, var, new_version)


if __name__ == u'__main__':
    cli()
