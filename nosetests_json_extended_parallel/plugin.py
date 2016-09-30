
from __future__ import absolute_import

import traceback
from collections import namedtuple
from nose.plugins import Plugin
from multiprocessing import Manager

from nosetests_json_extended_parallel.sink import Sink


class JsonExtendedPlugin(Plugin):
    name = 'json-extended-parallel'
    score = 2000

    def options(self, parser, env):
        Plugin.options(self, parser, env)

    def configure(self, options, config):
        Plugin.configure(self, options, config)

        self.config = config
        if not self.enabled:
            return

        self._sink = Sink()
        if not hasattr(self.config, '_nose_json_extended_state_'):
            manager = Manager()
            self._sink.records = manager.list()
            self.config._nose_json_extended_state_ = self._sink.records
        else:
            self._sink.records = self.config._nose_json_extended_state_

    def report(self, stream):
        self._sink.write()

    def addError(self, test, err, capt=None):
        if issubclass(err[0], SyntaxError):
            self._sink.add_syntaxerror(syntax_error_report(err[1]))
        else:
            self._sink.add('error',
                           testcase_description(test),
                           error_report(err))

    def addFailure(self, test, err, capt=None, tb_info=None):
        self._sink.add('failed',
                       testcase_description(test),
                       error_report(err))

    def addSuccess(self, test, capt=None):
        self._sink.add('success', testcase_description(test), None)


TestCaseDescription = namedtuple('TestCaseDescription',
                                 'module name filename linenr')


def testcase_description(test):

    module, name = _split_id(test.id())

    filename = None
    linenr = None

    try:
        filename = test.address()[0]
    except:
        pass

    try:
        methodname = test.test._testMethodName
        func = getattr(test.test, methodname)
        linenr = func.__func__.__code__.co_firstlineno
    except:
        pass

    return TestCaseDescription(module, name, filename, linenr)


ErrorReport = namedtuple('ErrorReport', 'message traceback')


def error_report(err):
    message_list = traceback.format_exception_only(err[0], err[1])
    message = '\n'.join(message_list).strip('\n')

    tb = list(wrap_traceback(traceback.extract_tb(err[2])))

    return ErrorReport(message, tb)


def wrap_traceback(traceback_in):
    names = ('filename', 'linenr', 'function', 'line')
    for tb in traceback_in:
        yield dict(zip(names, tb))


def _split_id(test_id):
    parts = test_id.split('.')
    return '.'.join(parts[:-1]), parts[-1]




SyntaxErrorReport = namedtuple('SyntaxErrorReport', 'filename linenr column message')

def syntax_error_report(error):
    filename = error.filename
    linenr = error.lineno
    column = error.offset

    message = error.__class__.__name__ + ': ' + str(error)

    if error.text:
        message += '\n\n' + error.text.strip()

        if error.offset:
            text = error.text.rstrip()
            nr_white_space = len(text) - len(text.lstrip())
            nr = error.offset-nr_white_space-1
            message += '\n' + ' ' * nr + '^'

    return SyntaxErrorReport(filename, linenr, column, message)
