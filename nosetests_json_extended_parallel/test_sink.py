from __future__ import absolute_import

import unittest

from nosetests_json_extended_parallel.sink import Sink
from nosetests_json_extended_parallel.plugin import TestCaseDescription as TC
from nosetests_json_extended_parallel.plugin import SyntaxErrorReport
from nosetests_json_extended_parallel.plugin import ErrorReport


class SinkTest(unittest.TestCase):

    def test_module_headers(self):
        sink = Sink()
        sink.add('success', TC('module.A', 'test1', None, None), None)
        sink.add('success', TC('module.A', 'test2', None, None), None)
        sink.add('success', TC('module.B', 'test3', None, None), None)
        sink.add('failed', TC('module.B', 'test4', None, None), None)
        sink.add('success', TC('module.C', 'test5', None, None), None)
        sink.add('error', TC('module.C', 'test6', None, None), None)
        sink.add_syntaxerror(SyntaxErrorReport('file.py', 3, 4, 'msg'))

        out = sink.generate()

        self.assertEqual(out['modules'][0]['name'], 'module.A')
        self.assertEqual(out['modules'][0]['nr_success'], 2)
        self.assertEqual(out['modules'][0]['nr_failed'], 0)
        self.assertEqual(out['modules'][0]['nr_error'], 0)

        self.assertEqual(out['modules'][1]['name'], 'module.B')
        self.assertEqual(out['modules'][1]['nr_success'], 1)
        self.assertEqual(out['modules'][1]['nr_failed'], 1)
        self.assertEqual(out['modules'][1]['nr_error'], 0)

        self.assertEqual(out['modules'][2]['name'], 'module.C')
        self.assertEqual(out['modules'][2]['nr_success'], 1)
        self.assertEqual(out['modules'][2]['nr_failed'], 0)
        self.assertEqual(out['modules'][2]['nr_error'], 1)

    def _single_testcase(self, *a):
        sink = Sink()
        sink.add(*a)
        return sink.generate()

    def test_testcase_success(self):
        tc = TC('mod', 'test1', None, None)
        out = self._single_testcase('success', tc, None)
        tc1 = out['modules'][0]['testcases'][0]
        self.assertEqual(tc1['name'], 'test1')
        self.assertEqual(tc1['result'], 'success')

    def test_testcase_failed(self):
        er = ErrorReport('error_desc', ['tb0', 'tb1'])
        tc = TC('mod', 'test1', None, None)
        out = self._single_testcase('error', tc, er)
        tc1 = out['modules'][0]['testcases'][0]

        self.assertEqual(tc1['name'], 'test1')
        self.assertEqual(tc1['result'], 'error')
        self.assertEqual(tc1['error']['message'], 'error_desc')
        self.assertEqual(tc1['error']['traceback'], ['tb0', 'tb1'])

    def test_testcase_syntax(self):
        sink = Sink()
        sink.add_syntaxerror(SyntaxErrorReport('filename', 6, 18, 'message'))
        out = sink.generate()

        expected = dict(name='filename',
                        error=dict(message='message',
                                   traceback=[dict(filename='filename',
                                                   linenr=6,
                                                   column=18)]))

        self.assertEqual(out['syntaxerrors'], [expected])


class SyntaxTest(unittest.TestCase):

    def test_module_headers(self):
        pass
