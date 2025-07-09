#!/usr/bin/env python3

import argparse
import subprocess
import sys
import os
import re

# The Makefile is expected to be in the current working directory
MAKEFILE_PATH = os.path.join(os.getcwd(), 'Makefile')


def parse_makefile_targets(makefile_path):
    """
    Parse the Makefile to extract targets and their descriptions.
    The description for each target is taken from the first comment (#) immediately above the target definition.
    """
    targets = {}
    pattern = re.compile(r'^([\w%\-]+):')

    with open(makefile_path, 'r') as mf:
        lines = mf.readlines()

    for idx, line in enumerate(lines):
        match = pattern.match(line)
        if match:
            target = match.group(1)
            # Look upwards for the first non-empty comment
            desc = None
            for prev in range(idx - 1, -1, -1):
                prev_line = lines[prev].strip()
                if prev_line.startswith('#'):
                    desc = prev_line.lstrip('# ').strip()
                    break
                if prev_line:
                    # Stop if a non-comment non-empty line encountered
                    break
            targets[target] = desc or ''
    return targets


def run_make_command(command):
    """Runs the make command with the given target and streams output in real-time."""
    # Change working directory to where Makefile resides
    os.chdir(os.getcwd())

    try:
        process = subprocess.Popen(['make', command], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        for line in process.stdout:
            print(line.decode(), end='')
        for line in process.stderr:
            print(line.decode(), end='', file=sys.stderr)
        process.wait()
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e.stderr.decode()}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Proxy to all Makefile targets with auto-generated help from Makefile comments"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available Makefile targets")

    # Dynamically add subcommands for each Makefile target
    targets = parse_makefile_targets(MAKEFILE_PATH)
    for target, desc in targets.items():
        subparsers.add_parser(target, help=desc)

    args = parser.parse_args()

    if args.command:
        run_make_command(args.command)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
