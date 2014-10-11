"""Hello World example utilizing ComponentCore"""
from cognate.component_core import ComponentCore

import sys


class HelloWorld(ComponentCore):
    def __init__(self, name='World', **kwargs):
        self.name = name

        ComponentCore.__init__(self, **kwargs)

    def cognate_options(self, arg_parser):
        arg_parser.add_argument(
            '--name',
            default=self.name,
            help='Whom will receive the salutation.')

    def run(self):
        self.log.info('Hello %s', self.name)


if __name__ == '__main__':
    argv = sys.argv
    service = HelloWorld(argv=argv)
    service.run()
