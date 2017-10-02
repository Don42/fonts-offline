#!/usr/env/python3
# ----------------------------------------------------------------------------
# "THE SCOTCH-WARE LICENSE" (Revision 42):
# <don@0xbeef.org> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a scotch whisky in return
# Marco 'don' Kaulea
# ----------------------------------------------------------------------------

from fonts_offline import css_downloader
import requests
import requests_mock
import pytest
import os
import os.path
import shutil
import unittest


def test_download_css():
    with requests_mock.mock() as m:
        test_url = 'http://example.com/test.css'
        m.get(test_url, text='data')
        assert css_downloader.download_css({}, test_url) == 'data'
        assert m.call_count == 1


def test_download_css_fail():
    with requests_mock.mock() as m:
        test_url = 'http://example.com/test.css'
        m.get(test_url, text='data', status_code=400)
        with pytest.raises(requests.exceptions.HTTPError):
            css_downloader.download_css({}, test_url) == 'data'
        assert m.call_count == 1


class FileTestCases(unittest.TestCase):

    def setUp(self):
        if os.path.exists("/tmp/fonts-offline"):
            shutil.rmtree("/tmp/fonts-offline")
        os.mkdir("/tmp/fonts-offline")

    def tearDown(self):
        shutil.rmtree("/tmp/fonts-offline")

    def test_get_font_file_empty(self):
        with requests_mock.mock() as m:
            test_url = 'http://example.com/fonts/test.ttf'
            data = ''
            ttf = '/tmp/fonts-offline/font_Roboto_Regular_400.ttf'
            m.get(test_url, text=data, status_code=200)
            output = css_downloader.get_font_file(test_url,
                                                  ttf,
                                                  {})
            assert output is None
            assert m.call_count == 1
            request = m.request_history[0]
            assert request.method == 'GET'
            assert request.url == test_url
            assert os.path.isfile(ttf)
            with open(ttf, 'r') as file:
                assert file.read() == data

    def test_get_font_file(self):
        with requests_mock.mock() as m:
            test_url = 'http://example.com/fonts/test.ttf'
            data = '''
IN the year 1878 I took my degree of Doctor of Medicine of the
University of London, and proceeded to Netley to go through the course
prescribed for surgeons in the army. Having completed my studies there,
I was duly attached to the Fifth Northumberland Fusiliers as Assistant
Surgeon. The regiment was stationed in India at the time, and before
I could join it, the second Afghan war had broken out. On landing at
Bombay, I learned that my corps had advanced through the passes, and
was already deep in the enemy's country. I followed, however, with many
other officers who were in the same situation as myself, and succeeded
in reaching Candahar in safety, where I found my regiment, and at once
entered upon my new duties.

The campaign brought honours and promotion to many, but for me it had
nothing but misfortune and disaster. I was removed from my brigade and
attached to the Berkshires, with whom I served at the fatal battle of
Maiwand. There I was struck on the shoulder by a Jezail bullet, which
shattered the bone and grazed the subclavian artery. I should have
fallen into the hands of the murderous Ghazis had it not been for the
devotion and courage shown by Murray, my orderly, who threw me across a
pack-horse, and succeeded in bringing me safely to the British lines.

Worn with pain, and weak from the prolonged hardships which I had
undergone, I was removed, with a great train of wounded sufferers, to
the base hospital at Peshawar. Here I rallied, and had already improved
so far as to be able to walk about the wards, and even to bask a little
upon the verandah, when I was struck down by enteric fever, that curse
of our Indian possessions. For months my life was despaired of, and
when at last I came to myself and became convalescent, I was so weak and
emaciated that a medical board determined that not a day should be lost
in sending me back to England. I was dispatched, accordingly, in the
troopship "Orontes," and landed a month later on Portsmouth jetty, with
my health irretrievably ruined, but with permission from a paternal
government to spend the next nine months in attempting to improve it.
            '''
            ttf = '/tmp/fonts-offline/font_Roboto_Regular_400.ttf'
            m.get(test_url, text=data, status_code=200)
            output = css_downloader.get_font_file(test_url,
                                                  ttf,
                                                  {})
            assert output is None
            assert m.call_count == 1
            request = m.request_history[0]
            assert request.method == 'GET'
            assert request.url == test_url
            assert os.path.isfile(ttf)
            with open(ttf, 'r') as file:
                assert file.read() == data

    def test_get_font_file_fail(self):
        with requests_mock.mock() as m:
            test_url = 'http://example.com/fonts/test.ttf'
            data = ''
            ttf = '/tmp/fonts-offline/font_Roboto_Regular_400.ttf'
            m.get(test_url, text=data, status_code=400)
            with pytest.raises(Exception):
                css_downloader.get_font_file(test_url, ttf, {})
            assert m.call_count == 1
            request = m.request_history[0]
            assert request.method == 'GET'
            assert request.url == test_url
            assert not os.path.exists(ttf)
