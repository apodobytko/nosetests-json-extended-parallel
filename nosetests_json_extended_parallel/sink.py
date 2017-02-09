from datetime import datetime
import json


class Sink:
    def __init__(self):
        self.results = []
        self.syntaxerrors = []
        self.output_file = 'nosetests.json'
        self.start_time = datetime.utcnow()
        self.stats = {
            'errors': 0,
            'failures': 0,
            'passes': 0,
            'skipped': 0,
        }

    def write(self):
        end_time = datetime.utcnow()
        total = end_time - self.start_time
        output = {
            'start_time': '{} UTC'.format(self.start_time),
            'end_time': '{} UTC'.format(end_time),
            'total': str(total),
            'stats': self.stats._getvalue(),
            'results': self.results._getvalue(),
        }
        with open(self.output_file, 'w') as f:
            json.dump(output, f)
