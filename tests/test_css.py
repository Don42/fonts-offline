#!/usr/env/python3
# ----------------------------------------------------------------------------
# "THE SCOTCH-WARE LICENSE" (Revision 42):
# <DonMarco42@gmail.com> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a scotch whisky in return
# Marco 'don' Kaulea
# ----------------------------------------------------------------------------

import unittest

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

    def test_get_style(self):
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
