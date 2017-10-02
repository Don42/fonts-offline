#!/usr/env/python3
# ----------------------------------------------------------------------------
# "THE SCOTCH-WARE LICENSE" (Revision 42):
# <don@0xbeef.org> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a scotch whisky in return
# Marco 'don' Kaulea
# ----------------------------------------------------------------------------

import unittest
try:
    from unittest import mock
except ImportError:
    from mock import mock

import fonts_offline


class InitTestCase(unittest.TestCase):
    @mock.patch('fonts_offline.css_downloader')
    @mock.patch('docopt.docopt')
    def test_main_ttf(self, doc, downloader):
        doc.return_value = {'--ttf': True, '<url>': 'This is the url'}
        downloader.process_css_url.return_value = 'This is css'
        fonts_offline.main()
        assert doc.call_count == 1
        downloader.process_css_url.assert_called_once_with('This is the url',
                                                           {},
                                                           '')

    @mock.patch('fonts_offline.css_downloader')
    @mock.patch('docopt.docopt')
    def test_main(self, doc, downloader):
        doc.return_value = {'--ttf': False, '<url>': 'This is the url'}
        downloader.process_css_url.return_value = 'This is css'
        fonts_offline.main()
        assert doc.call_count == 1
        downloader.process_css_url.assert_called_once_with(
            'This is the url',
            {'User-agent': ('User-Agent: Mozilla/5.0 (X11;'
                            ' Linux x86_64; rv:38.0) Gecko/20100101'
                            'Firefox/38.0 Iceweasel/38.1.0')},
            '')

    @mock.patch('fonts_offline.css_downloader')
    @mock.patch('docopt.docopt')
    def test_main_ttf_with_path(self, doc, downloader):
        doc.return_value = {'--ttf': True,
                            '<url>': 'This is the url',
                            '--font-path': 'path/to/fonts'}
        downloader.process_css_url.return_value = 'This is css'
        fonts_offline.main()
        assert doc.call_count == 1
        downloader.process_css_url.assert_called_once_with('This is the url',
                                                           {},
                                                           'path/to/fonts')

    @mock.patch('fonts_offline.css_downloader')
    @mock.patch('docopt.docopt')
    def test_main_with_path(self, doc, downloader):
        doc.return_value = {'--ttf': False,
                            '<url>': 'This is the url',
                            '--font-path': 'path/to/fonts'}
        downloader.process_css_url.return_value = 'This is css'
        fonts_offline.main()
        assert doc.call_count == 1
        downloader.process_css_url.assert_called_once_with(
            'This is the url',
            {'User-agent': ('User-Agent: Mozilla/5.0 (X11;'
                            ' Linux x86_64; rv:38.0) Gecko/20100101'
                            'Firefox/38.0 Iceweasel/38.1.0')},
            'path/to/fonts')

