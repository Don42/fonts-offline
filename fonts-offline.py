#!/usr/bin/env python3
# ----------------------------------------------------------------------------
# "THE SCOTCH-WARE LICENSE" (Revision 42):
# <DonMarco42@gmail.com> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a scotch whisky in return
# Marco 'don' Kaulea
# ----------------------------------------------------------------------------

'''Download recipes

Usage:
    fonts-offline [--ttf] [--font-path=<PATH>] <url>
'''
import docopt
import pathlib as pl
import re
import requests


def get_urls(css):
    match = re.findall('url\(([^)]*)\)', css, re.MULTILINE)
    return match


def get_family(css):
    match = re.search('font-family: \'([^\']*)\';', css)
    if match:
        return match.group(1)
    raise Exception("Font-Family not found")


def get_style(css):
    match = re.search('font-style: ([^;]*);', css)
    if match:
        return match.group(1)
    raise Exception("Font-Style not found")


def get_weight(css):
    match = re.search('font-weight: ([^;]*);', css)
    if match:
        return match.group(1)
    raise Exception("Font-Weight not found")


def get_font_file(url, local_filename,  headers):
    r = requests.get(url, headers=headers, stream=True)
    if not r.ok:
        raise Exception("Error while retrieving font")
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()
    return local_filename


def build_local_filenames(font_def, font_path=''):
    template = 'font_{family}_{style}_{weight}.{type}'
    local_filenames = list()
    for url in font_def['urls']:
        filename = template.format(family=font_def['font-family'],
                                   style=font_def['font-style'],
                                   weight=font_def['font-weight'],
                                   type=url.split('.')[-1])
        filepath = pl.Path(font_path) / filename
        local_filenames.append(str(filepath))
    return local_filenames


def extract_information(main_css):
    font_faces = main_css.split('@')
    ret = list()
    for font_face in font_faces:
        if not font_face:
            continue
        font_def = dict()
        font_def['font-family'] = get_family(font_face)
        font_def['font-style'] = get_style(font_face)
        font_def['font-weight'] = get_weight(font_face)
        font_def['urls'] = get_urls(font_face)
        ret.append(font_def)
    return ret


def replace_url(css, url, local_filename):
    return css.replace(url, local_filename)


def main():
    arguments = docopt.docopt(__doc__)
    headers = {'User-agent': ('User-Agent: Mozilla/5.0 (X11;'
                              ' Linux x86_64; rv:38.0) Gecko/20100101'
                              'Firefox/38.0 Iceweasel/38.1.0')}
    if '--ttf' in arguments and arguments['--ttf']:
        headers = {}
    font_path = arguments['--font-path'] if '--font-path' in arguments else ''
    result = requests.get(arguments['<url>'], headers=headers)
    result.encoding = 'utf-8'
    main_css = result.text
    font_defs = extract_information(main_css)
    output_css = main_css
    for font in font_defs:
        font['local_filenames'] = build_local_filenames(font, font_path)
        for url, filename in zip(font['urls'], font['local_filenames']):
            get_font_file(url, filename, headers)
            output_css = replace_url(output_css, url, filename)
    print(output_css)

if __name__ == "__main__":
    main()
