from datetime import datetime
from multiprocessing import Manager
from time import time

from nose.exc import SkipTest
from nose.plugins import Plugin
from nose.plugins.xunit import id_split, format_exception
from nosetests_json_extended_parallel.sink import Sink


class JsonExtendedPlugin(Plugin):
    name = 'jsonmp'
    score = 2000

    def options(self, parser, env):
        Plugin.options(self, parser, env)
        parser.add_option("--jsonmp-file", action="store",
                default=env.get('NOSE_JSONMP_OUTPUT_FILE', 'nosetests.json'),
                dest="jsonmp_file",
                metavar="FILE",
                help="save results in the specified JSON file."
                "[NOSE_JSONMP_OUTPUT_FILE]" )

    def configure(self, options, config):
        Plugin.configure(self, options, config)

        self.config = config
        if not self.enabled:
            return

        self._sink = Sink()
        if not hasattr(self.config, '_nose_jsonmp_extended_state_'):
            manager = Manager()
            self._sink.results = manager.list()
            self._sink.stats = manager.dict(**self._sink.stats)
            self.config._nose_jsonmp_extended_state_ = self._sink.results, self._sink.stats
        else:
            self._sink.results, self._sink.stats = self.config._nose_jsonmp_extended_state_
        self._sink.output_file=options.jsonmp_file

    def startTest(self, test):
        self._timer = time()

    def _get_time_taken(self):
        if hasattr(self, '_timer'):
            taken = time() - self._timer
        else:
            taken = 0.0
        return taken

    def report(self, stream):
        self._sink.write()

    def addError(self, test, err, capt=None):
        taken = self._get_time_taken()

        if issubclass(err[0], SkipTest):
            status = 'skipped'
            self._sink.stats['skipped'] += 1
        else:
            status = 'error'
            self._sink.stats['errors'] += 1
        tb = format_exception(err)
        test_id = test.id()
        name = id_split(test_id)[-1]
        started = getattr(self, '_timer', time())
        ended = started + taken
        self._sink.results.append({
            'id': test_id,
            'name': name,
            'time': taken,
            'status': status,
            'started': datetime.fromtimestamp(started).strftime('%x %X'),
            'ended': datetime.fromtimestamp(ended).strftime('%x %X'),
            'tb': tb,
        })

    def addFailure(self, test, err, capt=None, tb_info=None):
        taken = self._get_time_taken()
        tb = format_exception(err)
        self._sink.stats['failures'] += 1
        test_id = test.id()
        name = id_split(test_id)[-1]
        started = getattr(self, '_timer', time())
        ended = started + taken
        self._sink.results.append({
            'id': test_id,
            'name': name,
            'time': taken,
            'status': 'failure',
            'started': datetime.fromtimestamp(started).strftime('%x %X'),
            'ended': datetime.fromtimestamp(ended).strftime('%x %X'),
            'tb': tb,
        })

    def addSuccess(self, test, capt=None):
        taken = self._get_time_taken()
        self._sink.stats['passes'] += 1
        test_id = test.id()
        name = id_split(test_id)[-1]
        started = getattr(self, '_timer', time())
        ended = started + taken
        self._sink.results.append({
            'id': test_id,
            'name': name,
            'time': taken,
            'status': 'success',
            'started': datetime.fromtimestamp(started).strftime('%x %X'),
            'ended': datetime.fromtimestamp(ended).strftime('%x %X'),
        })
