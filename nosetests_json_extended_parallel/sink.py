import json
import os
import sys
import time

from collections import Counter
from operator import itemgetter, attrgetter



class TestCase:
    def __init__(self, result, testcase, error):
        self.result = result
        self.testcase = testcase
        self.error = error

    def to_dict(self):
        out = dict(name=self.testcase.name,
                   filename=self.testcase.filename,
                   linenr=self.testcase.linenr,
                   result=self.result)

        if self.error:
            out['error'] = dict(message=self.error.message,
                                traceback=self.error.traceback)

        return out


class Module:
    def __init__(self, name):
        self.name = name
        self.testcases = []

    def to_dict(self):

        # count the number succeeded, failed or error test cases
        result_counts = Counter(map(attrgetter('result'), self.testcases))

        # convert testcases to dicts
        testcases = list(map(lambda tc: tc.to_dict(), self.testcases))

        return dict(name=self.name,
                    nr_success=result_counts['success'],
                    nr_failed=result_counts['failed'],
                    nr_error=result_counts['error'],
                    testcases=testcases)


class Syntax:
    def __init__(self, error):
        self.filename = error.filename
        self.linenr = error.linenr
        self.column = error.column
        self.message = error.message

    def to_dict(self):
        tb = [dict(filename=self.filename,
                   linenr=self.linenr,
                   column=self.column)]
        out = dict(name=self.filename,
                   error=dict(message=self.message, traceback=tb))
        return out


class Sink:
    def __init__(self):
        self.records = []
        self.syntaxerrors = []
        self.output_file = 'nosetests.json'

    def write(self):
        output = self.generate()
        with open(self.output_file, 'w') as f:
            json.dump(output, f)

    def add(self, result, testcase, error):
        self.records.append(TestCase(result, testcase, error))

    def add_syntaxerror(self, error):
        self.syntaxerrors.append(Syntax(error))

    def generate(self):

        modules = {}

        for record in self.records:
            module_name = record.testcase.module

            if module_name not in modules:
                modules[module_name] = Module(module_name)

            module = modules[module_name]

            module.testcases.append(record)

        # Convert all modules to dicts
        modules_out = list(map(lambda m: m.to_dict(), modules.values()))
        modules_out.sort(key=itemgetter('name'))

        # Convert all syntax errors to dicts
        syntaxerrors = [error.to_dict() for error in self.syntaxerrors]

        return dict(metadata=self.metadata(),
                    syntaxerrors=syntaxerrors,
                    modules=modules_out)

    def metadata(self):
        return dict(command=' '.join(sys.argv),
                    time=time.time(),
                    cwd=os.getcwd())
