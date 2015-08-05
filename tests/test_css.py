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
        input_string = {'font-family': 'family',
                 'font-style': 'style',
                 'font-weight': 'weight',
                 'urls': ['http://example.com/path/to/file/font.ttf']}
        expected = ['font_family_style_weight.ttf']
        assert css_downloader.build_local_filenames(input_string) == expected

    def test_build_local_filenames_multi(self):
        input_string = {'font-family': 'family',
                 'font-style': 'style',
                 'font-weight': 'weight',
                 'urls': ['http://example.com/path/to/file/font.ttf',
                          'http://example.com/path/to/file/font.woff']}
        expected = ['font_family_style_weight.ttf',
                    'font_family_style_weight.woff']
        assert css_downloader.build_local_filenames(input_string) == expected

    def test_build_local_filenames_single_with_path(self):
        input_string = {'font-family': 'family',
                 'font-style': 'style',
                 'font-weight': 'weight',
                 'urls': ['http://example.com/path/to/file/font.ttf']}
        expected = ['fonts/font_family_style_weight.ttf']
        assert css_downloader.build_local_filenames(input_string, 'fonts/') == expected

    def test_build_local_filenames_multi_with_path(self):
        input_string = {'font-family': 'family',
                 'font-style': 'style',
                 'font-weight': 'weight',
                 'urls': ['http://example.com/path/to/file/font.ttf',
                          'http://example.com/path/to/file/font.woff']}
        expected = ['fonts/font_family_style_weight.ttf',
                    'fonts/font_family_style_weight.woff']
        assert css_downloader.build_local_filenames(input_string, 'fonts/') == expected

    def test_extract_information(self):
        input_string = """
        @font-face {
        font-family: 'Roboto Condensed';
        font-style: normal;
        font-weight: 400;
        src: local('Roboto Condensed'), local('RobotoCondensed-Regular'),
             url(http://fonts.gstatic.com/s/robotocondensed/v13/Zd2E9abXLFGSr9G3YK2MsDR-eWpsHSw83BRsAQElGgc.ttf) format('truetype');
        }
        @font-face {
        font-family: 'Roboto Slab';
        font-style: bold;
        font-weight: 700;
        src: local('Roboto Slab'), local('RobotoSlab-Bold'),
             url(http://fonts.gstatic.com/s/robotoslab/v13/Zd2E9abXLFGSr9G3YK2MsDR-eWpsHSw83BRsAQElGgc.ttf) format('truetype');
        }"""
        expected = [{'font-family': 'Roboto Condensed',
                     'font-style': 'normal',
                     'font-weight': '400',
                     'urls': ['http://fonts.gstatic.com/s/robotocondensed/v13/Zd2E9abXLFGSr9G3YK2MsDR-eWpsHSw83BRsAQElGgc.ttf']},
                    {'font-family': 'Roboto Slab',
                     'font-style': 'bold',
                     'font-weight': '700',
                     'urls': ['http://fonts.gstatic.com/s/robotoslab/v13/Zd2E9abXLFGSr9G3YK2MsDR-eWpsHSw83BRsAQElGgc.ttf']}]
        assert css_downloader.extract_information(input_string) == expected

    @mock.patch('fonts_offline.css_downloader.download_css')
    @mock.patch('fonts_offline.css_downloader.get_font_file')
    def test_process_css_url(self, get_font_file, download_css):
        """

        :type get_font_file: mock.Mock
        :type download_css: mock.Mock
        """
        input_url = 'http://fonts.example.org/fonts.css'
        input_header = {'Alpha': 'Bravo', 'Charlie': 'Delta'}
        input_font_path = './fonts/'
        download_css.return_value = (
            "@font-face {"
            "font-family: 'Roboto Condensed';"
            "font-style: normal;"
            "font-weight: 400;"
            "src: local('Roboto Condensed'), local('RobotoCondensed-Regular'),"
            "     url(http://fonts.gstatic.com/s/robotocondensed/v13/Zd2E9abXLFGSr9G3YK2MsDR-eWpsHSw83BRsAQElGgc.ttf) "
            "format('truetype');"
            "}"
            "@font-face {"
            "font-family: 'Roboto Slab';"
            "font-style: bold;"
            "font-weight: 700;"
            "src: local('Roboto Slab'), local('RobotoSlab-Bold'),"
            "     url(http://fonts.gstatic.com/s/robotoslab/v13/Zd2E9abXLFGSr9G3YK2MsDR-eWpsHSw83BRsAQElGgc.ttf) "
            "format('truetype');"
            "}")
        expected = ("@font-face {"
                    "font-family: 'Roboto Condensed';"
                    "font-style: normal;"
                    "font-weight: 400;"
                    "src: local('Roboto Condensed'), local('RobotoCondensed-Regular'),"
                    "     url(fonts/font_Roboto Condensed_normal_400.ttf) format('truetype');"
                    "}"
                    "@font-face {"
                    "font-family: 'Roboto Slab';"
                    "font-style: bold;"
                    "font-weight: 700;"
                    "src: local('Roboto Slab'), local('RobotoSlab-Bold'),"
                    "     url(fonts/font_Roboto Slab_bold_700.ttf) format('truetype');"
                    "}")
        output = css_downloader.process_css_url(input_url, input_header, input_font_path)
        assert output == expected
        download_css.assert_called_once_with(input_header, input_url)
        assert get_font_file.called
        assert get_font_file.call_count == 2
        expected_calls = [
            mock.call('http://fonts.gstatic.com/s/robotocondensed/v13/Zd2E9abXLFGSr9G3YK2MsDR-eWpsHSw83BRsAQElGgc.ttf',
                      'fonts/font_Roboto Condensed_normal_400.ttf',
                      input_header),
            mock.call('http://fonts.gstatic.com/s/robotoslab/v13/Zd2E9abXLFGSr9G3YK2MsDR-eWpsHSw83BRsAQElGgc.ttf',
                      'fonts/font_Roboto Slab_bold_700.ttf',
                      input_header)]
        assert get_font_file.mock_calls == expected_calls

    @mock.patch('fonts_offline.css_downloader.download_css')
    @mock.patch('fonts_offline.css_downloader.get_font_file')
    def test_process_css_url_empty(self, get_font_file, download_css):
        """

        :type get_font_file: mock.Mock
        :type download_css: mock.Mock
        """
        input_url = ''
        input_header = {}
        input_font_path = ''
        download_css.return_value = ''
        output = css_downloader.process_css_url(input_url, input_header, input_font_path)
        assert output == ''
        download_css.assert_called_once_with({}, '')
        assert not get_font_file.called
        assert get_font_file.call_count == 0
