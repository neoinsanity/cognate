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

        ComponentCore.__init__(self, **kwargs)

    def cognate_options(self, arg_parser):
        arg_parser.add_argument('-l',
                                default=self.lang,
                                choices=self.lang_choices,
                                help='Set the language for the salutation.')

    def greet(self, name='Mundo'):
        salutation = self.salutation_map[self.lang]
        greeting = salutation + ' ' + name
        self.log.debug('Greeting: %s', greeting)
        return greeting


if __name__ == '__main__':
    argv = sys.argv
    service = HolaMundo(argv=argv)

    while (True):
        name = raw_input('Enter name (No input quites):')
        if not name:
            break

        greeting = service.greet(name)
        print greeting
