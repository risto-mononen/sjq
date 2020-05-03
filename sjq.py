#! /usr/bin/env python3

"""Simple json query.  Like jq, but with prettier CLI syntax.

Mimic sql and output the matching (key, value) pairs as if running the
below sql query. Read only stdin.

select <keys> from <files> where <conditions>;

"""

import subprocess
import sys

_5tuple = 'src dst sport dport protocol'.split()

def runjq (compact=True, files=None, jqfilter='.', sorted=False, 
           input_string=None):
    cmd = ['jq', jqfilter]
    if files:
        cmd.extend(files)
    if compact:
        cmd.append('-c')
    if sorted:
        cmd.append('-s')
    if args.verbose:
        print(cmd)
    subprocess.run(cmd, input=input_string)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser('sjq')
    parser.add_argument('-k', '--keys', metavar='key',
                        nargs='*', default=_5tuple, #None,
                        help='List of JSON field names. Default all fields.')
    parser.add_argument('-c', '--conditions', metavar='expr',
                        nargs='*', default=None,
                        help='JSON field filter as a boolean expression, quote to avoid shell surprises. Default no filtering.')    
    parser.add_argument('-v', '--verbose', action='store_true')
    args = parser.parse_args()
    verbose = args.verbose
    if verbose:
        print(args)
    jqfilter = '.'
    if args.keys:
        jqfilter += ' | {%s}' % ', '.join(args.keys)
    if args.conditions:
        jqfilter += ' | select(.%s)' % ' AND '.join(args.conditions)
    runjq(jqfilter=jqfilter, files=None)
