import unittest
from setsuden4trac.reader import *
import os
import re
url_re = re.compile('http://api.gosetsuden.jp/(?P<command>[a-z]+)/.+')
class MockURLopener(object):
    commands = ['usage', 'peak']
    def __init__(self):
        self._code = None
    def open(self, url):
        cmd = url_re.match(url).group('command')
        if cmd in self.commands:
            return MockFile('./setsuden4trac/tests/%s.txt' % cmd, 200)
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
            self.assertEqual('Go setsuden@'+ region, reader.author()) 
    def testInvalidRegion(self):
        self.assertRaises(RegionError, Reader, 'nosuchregion')
    def testUsage(self):
        reader = Reader('kansai', opener=MockURLopener)
        result = reader.usage('instant', 'latest')
        self.assertEqual({ "code": 200, "usage":38770000,"timestamp":1313226300000},
          result)
        from datetime import datetime
        self.assertEqual("2011-08-13 18:05:00", 
          str(datetime.fromtimestamp(result['timestamp']/1000)))
    def test_InvalidCommand(self):
        reader = Reader('kansai')
        result = reader.nosuchcommand('instant', 'latest')
        self.assertEqual({'code': 404}, result)
    def test_getusage(self):
        reader = Reader('tokyo', opener=MockURLopener)
        result = reader.getusage()
        self.assertEqual(73, result['usage'])
        self.assertEqual('2011-08-13 18:05:00', str(result['datetime']))
