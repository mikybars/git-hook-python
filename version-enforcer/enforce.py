#!/usr/bin/env python3

import errno
import logging
import os
import subprocess
import sys
import yaml
from colorama import Fore, Style
from simple_term_menu import TerminalMenu

OPENAPI_REST_YML = 'rest/openapi-rest.yml'
METADATA_YML = 'rest/metadata.yml'

logger = logging.getLogger(__name__)


def bold(s):
    return f'{Style.BRIGHT}{s}{Style.RESET_ALL}'


def red(s):
    return f'{Fore.RED}{s}{Style.RESET_ALL}'


def green(s):
    return f'{Fore.GREEN}{s}{Style.RESET_ALL}'


def yellow(s):
    return f'{Fore.YELLOW}{s}{Style.RESET_ALL}'


def abort_push():
    print('Go change your version as desired and commit again before pushing')
    print(f'{red("Push aborted!")}')
    sys.exit(1)


def ask_confirmation(metadata_ver, openapi_ver):
    print(f'Version in metadata file [{yellow(metadata_ver)}] ' +
          f'is different from OpenAPI definition [{yellow(openapi_ver)}]')
    print(f'{green("?")} {bold("You OK with that?")}')
    if TerminalMenu(["[y] Yes", "[n] No"]).show() == 1:
        abort_push()


def file_content_at_rev(path, rev):
    git_cmd = ['git', 'show', f'{rev}:{path}']
    p = subprocess.run(git_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if len(p.stderr) > 0:
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), path)
    return p.stdout


def enforce(rev):
    try:
        metadata = yaml.load(file_content_at_rev(METADATA_YML, rev), Loader=yaml.FullLoader)
        metadata_ver = metadata['api']['version']

        openapi_rest = yaml.load(file_content_at_rev(OPENAPI_REST_YML, rev), Loader=yaml.FullLoader)
        openapi_ver = openapi_rest['info']['version']

        if metadata_ver != openapi_ver:
            ask_confirmation(metadata_ver, openapi_ver)
    except FileNotFoundError as ex:
        logger.warning(ex)


if __name__ == '__main__':
    _, local_sha, *_ = sys.stdin.readline().split()
    enforce(local_sha)
