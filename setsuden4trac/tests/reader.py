# -*- coding: utf-8 -*-
import unittest
from setsuden4trac.reader import *
import os
import re
from trac.util.datefmt import format_time, utc
url_re = re.compile('http://api.gosetsuden.jp/(?P<command>[a-z]+)/.+?/([a-z]+)/([a-z]+)')
class MockURLopener(object):
    commands = ['usage', 'peak']
    def __init__(self):
        self._code = None
    def open(self, url):
        m = url_re.match(url)
        if m.group('command') in self.commands:
            return MockFile('./setsuden4trac/tests/%s_%s_%s.txt' % m.groups(), 200)
        else:
            return MockFile('./setsuden4trac/tests/empty.txt', 404)
class MockFile(object):
    def __init__(self, path, code):
        self.fp = open(path, 'rb')
        self._code = code
    def getcode(self):
        return self._code
    def read(self):
        return self.fp.read()
    def close(self):
        self.fp.close()
    def fileno(self):
        return self.fp.fileno()
class ReaderTests(unittest.TestCase):
    def testConstructor(self):
        for region in ['tokyo', 'tohoku', 'kansai', 'kyushu', 'chubu']:
            reader = Reader(region)
            self.assertEqual(u'Go節電:'+ region, reader.author())
    def testInvalidRegion(self):
        self.assertRaises(RegionError, Reader, 'nosuchregion')
    def testUsage(self):
        reader = Reader('kansai', opener=MockURLopener)
        result = reader.usage('instant', 'latest')
        self.assertEqual({ "code": 200, "usage":38770000,"timestamp":1313226300000},
          result)
        from datetime import datetime
        dtime = datetime.fromtimestamp(result['timestamp']/1000, utc)
        self.assertEqual("18:05", format_time(dtime, str('%H:%M')))
    def test_InvalidCommand(self):
        reader = Reader('kansai')
        result = reader.nosuchcommand('instant', 'latest')
        self.assertEqual({'code': 404}, result)
    def test_getusage(self):
        reader = Reader('tokyo', opener=MockURLopener)
        result = reader.getusage()
        self.assertEqual(73, result['usage'])
        self.assertEqual(u'18:05', format_time(result['datetime'], str('%H:%M')))
        self.assertEqual(u'18', format_time(result['start'], str('%H'), utc))
        self.assertEqual(u'19', format_time(result['end'], str('%H'), utc))
