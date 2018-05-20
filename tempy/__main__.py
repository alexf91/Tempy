#
# Copyright 2018 Alexander Fasching
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

from __future__ import print_function
import argparse
import os
import sys
from collections import OrderedDict
import contextlib
import re
import traceback

from mako.template import Template

METAVARS = ('name', 'description', 'parser')

def load_file_template(filepath):
    """Load a template file and execute the metainfo part.
    Returns a tuple (metainfo, template) with metainfo as a dictionary
    and template Mako template.
    """
    with open(filepath) as fp:
        lines = fp.readlines()

    if lines[0] == '<<<\n':
        end = min([i for i, line in enumerate(lines) if line == '>>>\n'], default=None)
        if end is None:
            raise SyntaxError('Could not find enclosing >>>')

        # Extract the variables and create the template
        metacode = ''.join(lines[1:end])
        metainfo = run_metacode(metacode)
        template = Template(''.join(lines[end + 1:]))

    else:
        metainfo = {k: None for k in METAVARS}
        template = Template(''.join(lines))

    return metainfo, template


def load_directory_template(dirpath):
    """Load a template directory and execute the metainfo file.
    Returns a tuple (metainfo, {name: template}) with metainfo as a dictionary
    and the templates as a dictionary filename -> template.
    """
    metafile = os.path.join(dirpath, 'metainfo.py')
    if not os.path.exists(metafile):
        metainfo = {k: None for k in METAVARS}

    # Read the metacode
    with open(metafile) as fp:
        metacode = fp.read()

    # Extract the variables and read the templates
    metainfo = run_metacode(metacode)
    templates = {fname: Template(filename=os.path.join(dirpath, fname))
                    for fname in os.listdir(dirpath) if fname != 'metainfo.py'}

    return metainfo, templates


def run_metacode(metacode):
    """Run the metacode and return a dictionary with the metainfo."""
    # Execute the metacode
    loc = dict()
    glob = dict()
    exec(metacode, glob, loc)

    # Extract the variables and read the templates
    metainfo = {k: None for k in METAVARS}
    metainfo.update({k: v for k, v in loc.items() if k in METAVARS})

    return metainfo


def read_templates(tempydir, verbose=False):
    """Read all available templates from the tempy directory and return a
    triple (file/dirname, metainfo, templates).
    """
    if not os.path.exists(tempydir):
        return []

    results = []
    for fname in os.listdir(tempydir):
        path = os.path.join(tempydir, fname)
        try:
            if  os.path.isfile(path):
                metainfo, template = load_file_template(path)
                templates = {fname: template}
                results.append((fname, metainfo, templates))
            elif os.path.isdir(path):
                metainfo, templates = load_directory_template(path)
                results.append((fname, metainfo, templates))

        except Exception as e:
            if verbose:
                print('Exception in metacode section:', file=sys.stderr)
                traceback.print_exc()
            continue

    return results


def command_list(args):
    """List all available templates"""
    alltemplates = read_templates(args.tempydir, args.verbose)
    for fname, metainfo, templates in alltemplates:
        name = metainfo.get('name') or fname
        if metainfo['description']:
            formatstr = '{:<20}{:<}' if not args.m else '{}:{}'
            print(formatstr.format(name, metainfo['description']))
        else:
            formatstr = '{}' if not args.m else '{}:'
            print(formatstr.format(name))


def command_apply(args):
    """Create files or directory from a template."""
    alltemplates = read_templates(args.tempydir, args.verbose)
    # Find the correct template
    for nname, metainfo, templates in alltemplates:
        if (metainfo['name'] or nname) == args.name:
            break
    else:
        print('Template %s not found' % args.name, file=sys.stderr)
        return 1

    # Parse the template arguments
    parser = metainfo['parser']
    if parser is None:
        print('Template has no parser')
        return 1

    try:
        os.makedirs(args.output, exist_ok=True)
    except Exception as e:
        if args.verbose:
            traceback.print_exc()
        print('Could not create directory', file=sys.stderr)
        return 1

    targs = parser.parse_args(args.args)

    for name, template in templates.items():
        fname = name.format(**vars(targs))
        outpath = os.path.join(args.output, fname)
        if os.path.exists(outpath):
            if args.verbose:
                traceback.print_exc()
            print('Output file "%s" already exists' % outpath, file=sys.stderr)
            return 1

        try:
            content = template.render(**vars(targs))
            with open(outpath, 'w') as fp:
                fp.write(content)
        except Exception as e:
            if args.verbose:
                traceback.print_exc()
            print('Writing template output failed', file=sys.stderr)
            return 1


def main():
    parser = argparse.ArgumentParser(prog='tempy')
    parser.add_argument('--tempydir', '-t', type=str,
            default=os.path.expanduser('~/.tempy'),
            help='directory where templates are stored'
        )
    parser.add_argument('--verbose', '-v', action='store_true',
            help='print more output'
        )

    subparsers = parser.add_subparsers()

    # Parser for the 'list' command
    parser_list = subparsers.add_parser('list', help='list available templates')
    parser_list.set_defaults(func=command_list)
    # Option for machine readable output
    parser_list.add_argument('-m', action='store_true', help=argparse.SUPPRESS)

    # Parser for the 'apply' command
    parser_apply = subparsers.add_parser('apply',
            help='create file or directory from a template')
    parser_apply.add_argument('name', help='name of the template')
    parser_apply.add_argument('args', nargs='*',
            help='arguments for the template')
    parser_apply.add_argument('--output', '-o', default='.',
            help='output directory')
    parser_apply.set_defaults(func=command_apply)

    args = parser.parse_args()

    try:
        if 'func' in args:
            return args.func(args)
        else:
            parser.print_help()
            return 1
    except Exception as e:
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main() or 0)
