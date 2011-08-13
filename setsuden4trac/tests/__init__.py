from unittest import TestSuite, makeSuite

def test_suite():
    suite = TestSuite()
    import setsuden4trac.tests.reader
    suite.addTest(makeSuite(setsuden4trac.tests.reader.ReaderTests))
    return suite
