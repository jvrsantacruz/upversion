#!/bin/env python
# -*- coding: utf-8 -*-

import re
import click
import pkg_resources


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


def parse_version(path, var):
    """Parse major,minor,patch numbers"""
    with open(path) as stream:
        content = stream.read()

    match = compile_re(var).search(content)
    if match is None:
        error(u'Could not find \'{} = "x.x.x"\' in file "{}"', var, path)
    version = match.group('version')
    version = pkg_resources.parse_version(version).base_version

    numbers = list(map(int, version.split(u'.')))
    numbers += [0] * (len(numbers) - 3)  # complete N.N.N

    return tuple(numbers)


def string_version(version):
    return u'.'.join(map(str, version))


def write_version(path, var, version):
    r = compile_re(var)
    version = string_version(version)

    with open(path, 'r') as stream:
        content = stream.read()

    with open(path, 'w') as stream:
        stream.write(r.subn(r'\g<1>{}\g<3>'.format(version), content)[0])


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
    click.echo(u'From {} to {}'.format(
        string_version(version), string_version(new_version)))
    return new_version


def upversion(version, major, minor, patch):
    if major:
        version = version[0] + 1, 0, 0

    if minor:
        version = version[0], version[1] + 1, 0

    if patch:
        version = version[0], version[1], version[2] + 1

    return version


def check_number_arguments(major, minor, patch):
    if not (major or minor or patch):
        raise click.UsageError(
            u'Should specify at least one number to increase '
            u'use --major --minor --patch')


@cli.command()
@options
def view(path, var, major, minor, patch):
    check_number_arguments(major, minor, patch)
    change_version(parse_version(path, var), major, minor, patch)


@cli.command()
@options
def up(path, var, major, minor, patch):
    check_number_arguments(major, minor, patch)
    new_version = change_version(parse_version(path, var), major, minor, patch)
    click.secho(u'writing "{}"'.format(path), fg='yellow')
    write_version(path, var, new_version)


if __name__ == u'__main__':
    cli()
