from unittest import TestSuite, makeSuite

def test_suite():
    suite = TestSuite()
    import setsuden4trac.tests.reader
    suite.addTest(makeSuite(setsuden4trac.tests.reader.ReaderTests))
    import setsuden4trac.tests.core
    suite.addTest(makeSuite(setsuden4trac.tests.core.ComponentTests))
    return suite
