#!/usr/env/python3
# ----------------------------------------------------------------------------
# "THE SCOTCH-WARE LICENSE" (Revision 42):
# <DonMarco42@gmail.com> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a scotch whisky in return
# Marco 'don' Kaulea
# ----------------------------------------------------------------------------

from fonts_offline import css_downloader
import requests
import requests_mock
import pytest


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
