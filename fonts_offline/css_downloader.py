#!/usr/bin/env python3
# ----------------------------------------------------------------------------
# "THE SCOTCH-WARE LICENSE" (Revision 42):
# <don@0xbeef.org> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a scotch whisky in return
# Marco 'don' Kaulea
# ----------------------------------------------------------------------------

import pathlib as pl
import re
import requests


def get_urls(css):
    """
    Parse all URLs from a css font face declaration

    :param css: CSS containing one font face declaration
    :type css: str
    :return: URLs in the font declaration
    :rtype: list
    """
    match = re.findall('url\(([^)]*)\)', css, re.MULTILINE)
    return match


def get_family(css):
    """
    Parse the font family of a css font face declaration

    :param css: CSS containing one font face declaration
    :type css: str
    :return: Family of the font
    :rtype: str
    """
    match = re.search('font-family: \'([^\']*)\';', css)
    if match:
        return match.group(1)
    raise Exception("Font-Family not found")


def get_style(css):
    """
    Parse the font style of a css font face declaration

    :param css: CSS containing one font face declaration
    :type css: str
    :return: Style of the font
    :rtype: str
    """
    match = re.search('font-style: ([^;]*);', css)
    if match:
        return match.group(1)
    raise Exception("Font-Style not found")


def get_weight(css):
    """
    Parse the font weight of a css font face declaration

    :param css: CSS containing one font face declaration
    :type css: str
    :return: Weight of the font
    :rtype: str
    """
    match = re.search('font-weight: ([^;]*);', css)
    if match:
        return match.group(1)
    raise Exception("Font-Weight not found")


def get_font_file(url, local_filename,  headers):
    """
    Download font file and store it at using the provided file name

    :param url: URL to the font file
    :type url: str
    :param local_filename: Filename to store the font file
    :type local_filename: str
    :param headers: Headers to use in the request
    :type headers: dict
    :return: Local filename
    :rtype: str
    :raises:
        Exception: if there is an error while downloading
    """
    r = requests.get(url, headers=headers, stream=True)
    if not r.ok:
        raise Exception("Error while retrieving font")
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()


def download_css(headers, url):
    result = requests.get(url, headers=headers)
    result.raise_for_status()
    result.encoding = 'utf-8'
    main_css = result.text
    return main_css


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
        if not font_face or not font_face.strip():
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


def get_url_file_pairs(main_css, font_path):
    font_defs = extract_information(main_css)
    for font in font_defs:
        font['local_filenames'] = build_local_filenames(font, font_path)
        for pair in zip(font['urls'], font['local_filenames']):
            yield pair


def process_css_url(url, headers, font_path=''):
    main_css = download_css(headers, url)
    url_name_pairs = get_url_file_pairs(main_css, font_path)
    for url, filename in url_name_pairs:
        get_font_file(url, filename, headers)
        main_css = replace_url(main_css, url, filename)
    return main_css
