#!/usr/bin/env python3
# ----------------------------------------------------------------------------
# "THE SCOTCH-WARE LICENSE" (Revision 42):
# <DonMarco42@gmail.com> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a scotch whisky in return
# Marco 'don' Kaulea
# ----------------------------------------------------------------------------

"""Download fonts and create css to import them

Usage:
    fonts_offline [--ttf] [--font-path=<PATH>] <url>
"""
import docopt

from fonts_offline import css_downloader


def main():
    arguments = docopt.docopt(__doc__)
    if '--ttf' in arguments and arguments['--ttf']:
        headers = {}
    else:
        headers = {'User-agent': ('User-Agent: Mozilla/5.0 (X11;'
                                  ' Linux x86_64; rv:38.0) Gecko/20100101'
                                  'Firefox/38.0 Iceweasel/38.1.0')}

    font_path = arguments['--font-path'] if '--font-path' in arguments else ''
    print(css_downloader.process_css_url(arguments['<url>'],
                                         headers,
                                         font_path))
