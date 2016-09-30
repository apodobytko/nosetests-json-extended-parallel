from __future__ import absolute_import

import unittest
from nose.plugins import PluginTester
from nosetests_json_extended_parallel.plugin import (JsonExtendedPlugin, wrap_traceback,
                                            syntax_error_report)


class Helper(PluginTester, unittest.TestCase):
    activate = '--with-json-extended-parallel'
    plugins = [JsonExtendedPlugin()]

    def makeSuite(self):
        class Stub(unittest.TestCase):
            def runTest(tc):
                self.stubtest(tc)

        return [Stub('runTest')]

    @property
    def sink(self):
        return self.plugins[0]._sink


class SucceedsTest(Helper):

    def stubtest(self, tc):
        tc.assertTrue(True)

    def test(self):
        result = self.sink.records[0]

        self.assertEquals(result.result, 'success')
        self.assertEquals(result.testcase.module,
                          'nosetests_json_extended_parallel.test_plugin.Stub')
        self.assertEquals(result.testcase.name, 'runTest')
        self.assertEquals(result.error, None)
        self.assertEquals(result.testcase.filename[-14:], 'test_plugin.py')
        self.assertFalse(result.testcase.linenr is None)


class FailureTest(Helper):

    def stubtest(self, tc):
        tc.assertTrue(False)

    def test(self):
        result = self.sink.records[0]
        self.assertEquals(result.result, 'failed')
        message = 'AssertionError: False is not true'
        self.assertEquals(result.error.message, message)
        self.assertIsInstance(result.error.traceback, list)


class ErrorTest(Helper):

    def stubtest(self, tc):
        raise Exception('errormessage')

    def test(self):
        result = self.sink.records[0]
        self.assertEquals(result.result, 'error')
        self.assertEquals(result.error.message, 'Exception: errormessage')
        self.assertIsInstance(result.error.traceback, list)


class SyntaxErrorTest(Helper):

    def stubtest(self, tc):
        raise SyntaxError('errormessage')

    def test(self):
        result = self.sink.syntaxerrors[0]
        self.assertEquals(result.filename, None)
        self.assertEquals(result.linenr, None)
        self.assertEquals(result.column, None)
        self.assertEquals(result.message, 'SyntaxError: errormessage')


class TracebackWrapperTest(unittest.TestCase):

    def test(self):
        out = list(wrap_traceback([('file.py', 4, 'foo', 'bar()')]))

        self.assertEquals(out[0], dict(filename='file.py',
                                       linenr=4,
                                       function='foo',
                                       line='bar()'))


class SyntaxErrorReportTest(unittest.TestCase):

    def test(self):

        params = ('filename', 6, 18, '    def func(self)\n')
        report = syntax_error_report(SyntaxError('message', params))

        message = 'SyntaxError: message (filename, line 6)\n\n' \
                  'def func(self)\n             ^'

        self.assertEqual(report.filename, 'filename')
        self.assertEqual(report.linenr, 6)
        self.assertEqual(report.column, 18)
        self.assertEqual(report.message, message)
