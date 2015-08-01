#!/usr/env/python3
# ----------------------------------------------------------------------------
# "THE SCOTCH-WARE LICENSE" (Revision 42):
# <DonMarco42@gmail.com> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a scotch whisky in return
# Marco 'don' Kaulea
# ----------------------------------------------------------------------------

import unittest
try:
    from unittest import mock
except ImportError:
    from mock import mock

from fonts_offline import css_downloader
import fonts_offline


class CSSParserTest(unittest.TestCase):
    def test_get_urls(self):
        input_string = """url(http://example.com/path/to/file)"""
        expected = ['http://example.com/path/to/file']
        output = css_downloader.get_urls(input_string)
        self.assertListEqual(expected, output)

    def test_get_urls_broken(self):
        input_string = """url(http://example.com/path/to/file"""
        expected = []
        output = css_downloader.get_urls(input_string)
        self.assertListEqual(expected, output)

    def test_get_urls_multi(self):
        input_string = """
        @font-face {
        font-family: 'Roboto Condensed';
        font-style: normal;
        font-weight: 400;
        src: local('Roboto Condensed'), local('RobotoCondensed-Regular'),
        url(http://fonts.gstatic.com/s/robotocondensed/v13/Zd2E9abXLFGSr9G3YK2MsDR-eWpsHSw83BRsAQElGgc.ttf) format('truetype');
        }
        @font-face {
        font-family: 'Roboto Condensed';
        font-style: normal;
        font-weight: 700;
        src: local('Roboto Condensed Bold'), local('RobotoCondensed-Bold'),
        url(http://fonts.gstatic.com/s/robotocondensed/v13/b9QBgL0iMZfDSpmcXcE8nDokq8qT6AIiNJ07Vf_NrVA.ttf) format('truetype');
        }
        """
        expected = ['http://fonts.gstatic.com/s/robotocondensed/v13/Zd2E9abXLFGSr9G3YK2MsDR-eWpsHSw83BRsAQElGgc.ttf',
                    'http://fonts.gstatic.com/s/robotocondensed/v13/b9QBgL0iMZfDSpmcXcE8nDokq8qT6AIiNJ07Vf_NrVA.ttf']
        output = css_downloader.get_urls(input_string)
        self.assertListEqual(expected, output)

    def test_get_family(self):
        input_string = """
        @font-face {
        font-family: 'Roboto Condensed';
        font-style: normal;
        font-weight: 400;
        src: local('Roboto Condensed'), local('RobotoCondensed-Regular'),
        url(http://fonts.gstatic.com/s/robotocondensed/v13/Zd2E9abXLFGSr9G3YK2MsDR-eWpsHSw83BRsAQElGgc.ttf) format('truetype');
        }"""
        expected = 'Roboto Condensed'
        output = css_downloader.get_family(input_string)
        self.assertEqual(expected, output)

    def test_get_family_broken(self):
        input_string = """
        @font-face {
        font-famiy: 'Roboto Condensed';
        font-style: normal;
        font-weight: 400;
        src: local('Roboto Condensed'), local('RobotoCondensed-Regular'),
        url(http://fonts.gstatic.com/s/robotocondensed/v13/Zd2E9abXLFGSr9G3YK2MsDR-eWpsHSw83BRsAQElGgc.ttf) format('truetype');
        }"""
        self.assertRaises(Exception, css_downloader.get_family, input_string)

    def test_get_style(self):
        input_string = """
        @font-face {
        font-family: 'Roboto Condensed';
        font-style: normal;
        font-weight: 400;
        src: local('Roboto Condensed'), local('RobotoCondensed-Regular'),
        url(http://fonts.gstatic.com/s/robotocondensed/v13/Zd2E9abXLFGSr9G3YK2MsDR-eWpsHSw83BRsAQElGgc.ttf) format('truetype');
        }"""
        expected = 'normal'
        output = css_downloader.get_style(input_string)
        self.assertEqual(expected, output)

    def test_get_style_broken(self):
        input_string = """
        @font-face {
        font-family: 'Roboto Condensed';
        font-stye: normal;
        font-weight: 400;
        src: local('Roboto Condensed'), local('RobotoCondensed-Regular'),
        url(http://fonts.gstatic.com/s/robotocondensed/v13/Zd2E9abXLFGSr9G3YK2MsDR-eWpsHSw83BRsAQElGgc.ttf) format('truetype');
        }"""
        self.assertRaises(Exception, css_downloader.get_style, input_string)

    def test_get_weight(self):
        input_string = """
        @font-face {
        font-family: 'Roboto Condensed';
        font-style: normal;
        font-weight: 400;
        src: local('Roboto Condensed'), local('RobotoCondensed-Regular'),
        url(http://fonts.gstatic.com/s/robotocondensed/v13/Zd2E9abXLFGSr9G3YK2MsDR-eWpsHSw83BRsAQElGgc.ttf) format('truetype');
        }"""
        expected = '400'
        output = css_downloader.get_weight(input_string)
        self.assertEqual(expected, output)

    def test_get_weight_broken(self):
        input_string = """
        @font-face {
        font-family: 'Roboto Condensed';
        font-style: normal;
        font-weiht: 400;
        src: local('Roboto Condensed'), local('RobotoCondensed-Regular'),
        url(http://fonts.gstatic.com/s/robotocondensed/v13/Zd2E9abXLFGSr9G3YK2MsDR-eWpsHSw83BRsAQElGgc.ttf) format('truetype');
        }"""
        self.assertRaises(Exception, css_downloader.get_weight, input_string)

    def test_replace_url(self):
        input_string = "https://www.youtube.com/watch?v=q06xDugyxiw&list=PLp-wjw6lssYmrRD6jb2mMhpAYg8_kyS7-&index=19"
        expected = "this_is_a_file.ttf"
        output = css_downloader.replace_url(input_string,
                                            ("https://www.youtube.com/watch?v=q06xDugyxiw&list="
                                             "PLp-wjw6lssYmrRD6jb2mMhpAYg8_kyS7-&index=19"),
                                            "this_is_a_file.ttf")
        self.assertEqual(expected, output)
        expected = "this_is_a_file.wopr"
        output = css_downloader.replace_url(input_string,
                                            ("https://www.youtube.com/watch?v=q06xDugyxiw&list="
                                             "PLp-wjw6lssYmrRD6jb2mMhpAYg8_kyS7-&index=19"),
                                            "this_is_a_file.wopr")
        self.assertEqual(expected, output)

    def test_replace_url_multiline(self):
        input_string = """
        @font-face {
        font-family: 'Roboto Condensed';
        font-style: normal;
        font-weiht: 400;
        src: local('Roboto Condensed'), local('RobotoCondensed-Regular'),
        url(http://fonts.gstatic.com/s/robotocondensed/v13/Zd2E9abXLFGSr9G3YK2MsDR-eWpsHSw83BRsAQElGgc.ttf) format('truetype');
        }"""
        expected = """
        @font-face {
        font-family: 'Roboto Condensed';
        font-style: normal;
        font-weiht: 400;
        src: local('Roboto Condensed'), local('RobotoCondensed-Regular'),
        url(this_is_a_file.ttf) format('truetype');
        }"""
        output = css_downloader.replace_url(input_string,
                                            ("http://fonts.gstatic.com/s/robotocondensed/v13/"
                                             "Zd2E9abXLFGSr9G3YK2MsDR-eWpsHSw83BRsAQElGgc.ttf"),
                                            "this_is_a_file.ttf")
        self.assertEqual(expected, output)

    def test_build_local_filenames_single(self):
        input = {'font-family': 'family',
                 'font-style': 'style',
                 'font-weight': 'weight',
                 'urls': ['http://example.com/path/to/file/font.ttf']}
        expected = ['font_family_style_weight.ttf']
        assert css_downloader.build_local_filenames(input) == expected

    def test_build_local_filenames_multi(self):
        input = {'font-family': 'family',
                 'font-style': 'style',
                 'font-weight': 'weight',
                 'urls': ['http://example.com/path/to/file/font.ttf',
                          'http://example.com/path/to/file/font.woff']}
        expected = ['font_family_style_weight.ttf',
                    'font_family_style_weight.woff']
        assert css_downloader.build_local_filenames(input) == expected

    def test_build_local_filenames_single_with_path(self):
        input = {'font-family': 'family',
                 'font-style': 'style',
                 'font-weight': 'weight',
                 'urls': ['http://example.com/path/to/file/font.ttf']}
        expected = ['fonts/font_family_style_weight.ttf']
        assert css_downloader.build_local_filenames(input, 'fonts/') == expected

    def test_build_local_filenames_multi_with_path(self):
        input = {'font-family': 'family',
                 'font-style': 'style',
                 'font-weight': 'weight',
                 'urls': ['http://example.com/path/to/file/font.ttf',
                          'http://example.com/path/to/file/font.woff']}
        expected = ['fonts/font_family_style_weight.ttf',
                    'fonts/font_family_style_weight.woff']
        assert css_downloader.build_local_filenames(input, 'fonts/') == expected

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

