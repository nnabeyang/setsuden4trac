import unittest
from trac.core import ComponentManager
manager = ComponentManager()
from setsuden4trac.core import GoSetsudenComponent
from trac.config import Configuration
class Env(object):
    def __init__(self, fname):
        self.config = Configuration('./setsuden4trac/tests/%s' % fname)
 
class ComponentTests(unittest.TestCase):
    def test_env(self):       
        component = GoSetsudenComponent(manager)
        self.assertTrue(component.reader is None)
        setattr(component, 'env', Env('tokyo.ini'))
        component.set_reader()
        self.assertEqual(u'tokyo', component.reader.region)
        setattr(component, 'env', Env('empty.ini'))
        component.reader = None
        component.set_reader()
        self.assertEqual(u'kansai', component.reader.region)
 
