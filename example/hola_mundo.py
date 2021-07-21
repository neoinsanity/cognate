# coding=UTF-8
import sys
from cognate.component_core import ComponentCore


class HolaMundo(ComponentCore):
    salutation_map = {
        'Basque': u'Kaixo',
        'Chinese': u"Nǐ hǎo",
        'English': u'Hello',
        'French': u'Bonjour',
        'German': u'Hallo',
        'Hindi': u"Namastē",
        'Japanese': u"Kon'nichiwa",
        'Spanish': u'Hola',
    }

    lang_choices = salutation_map.keys()

    def __init__(self, lang='Spanish', **kwargs):
        self.lang = lang

        super().__init__(**kwargs)

    def cognate_options(self, arg_parser):
        arg_parser.add_argument('-l', '--lang',
                                default=self.lang,
                                choices=self.lang_choices,
                                help='Set the language for the salutation.')

    def cognate_configure(self, args):
        if self.lang not in self.lang_choices:
            msg = '"lang" value of %s not allowed.' % args.lang
            self.log.error(msg)
            raise ValueError(msg)

    def greet(self, name='Mundo'):
        if not name:
            name = 'Mundo'
        salutation = self.salutation_map[self.lang]
        greeting = salutation + ' ' + name
        self.log.debug('Greeting: %s', greeting)
        return greeting


if __name__ == '__main__':
    argv = sys.argv
    service = HolaMundo(argv=argv)

    while (True):
        name = input('Enter name ("quit" exits):')
        if name == 'quit':
            break

        greeting = service.greet(name)
        print(greeting)
