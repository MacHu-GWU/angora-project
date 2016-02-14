#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
requires: requests, chardet
"""

from __future__ import print_function
from .downloader import download_url
from .simplecrawler import (
    SmartDecoder, smtdecoder, SimpleCrawler, spider)