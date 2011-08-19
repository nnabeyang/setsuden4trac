# -*- coding: utf-8 -*-
import urllib
import os
from datetime import datetime
from trac.util.datefmt import utc, _tzmap
class Reader(object):
    regions = [
        'tokyo', 
        'tohoku',
        'kansai',
        'kyushu',
        'chubu',
        ]
    def __init__(self, region, opener=urllib.FancyURLopener):
        if not region in self.regions:
            raise RegionError()
        self.region = region
        self.opener = opener()
    def author(self):
        return u'Go節電:'+ self.region
    def getusage(self):
        usage = self.usage('instant', 'latest')
        use = usage['usage']
        time = datetime.fromtimestamp(usage['timestamp']/1000, utc)
        supply = self.peak('supply', 'today')['usage']
        demand_data = self.peak('demand', 'today')
        usage = float(use)/float(supply) * 100
        demand = float(demand_data['usage'])/float(supply) * 100
        start = datetime.fromtimestamp(demand_data['start'], utc)
        end = datetime.fromtimestamp(demand_data['end'], utc)
        return {'usage': int(usage), 'datetime': time, 'demand': demand,
                'start': start, 'end': end}
    def __getattr__(self, name):
        return lambda *args: self._exec_command(name, *args)
    def _exec_command(self, name, *args):
        open_url = self.opener.open(self._geturl(name, args))
        code = open_url.getcode()
        result = {'code': code}
        if code == 200:
            fp = os.fdopen(open_url.fileno())
            code = "result = %s" % fp.read()
            fp.close()
            namespace = {}
            exec code in namespace
            result.update(namespace['result'][0])
            return result
        else:
            open_url.close()
            return result
    def _geturl(self, name, args):        
        buf = ["http://api.gosetsuden.jp"]
        buf.extend([name, self.region])
        buf.extend(args)
        return '/'.join(buf)
class RegionError(Exception):
    pass
