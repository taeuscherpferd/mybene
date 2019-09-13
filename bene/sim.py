import logging
import os
import sys

from . import scheduler

TERM_COLOR_RESET = '\033[0m'
TERM_COLOR_RED = '\033[31m'
TERM_COLOR_GREEN = '\033[32m'
TERM_COLOR_YELLOW = '\033[33m'
TERM_COLOR_BLUE = '\033[34m'
TERM_COLOR_MAGENTA = '\033[35m'
TERM_COLOR_CYAN = '\033[36m'
TERM_COLOR_WHITE = '\033[37m'

class SimTimeFilter(logging.Filter):
    def filter(self, record):
        ct = Sim.scheduler.current_time()
        record.created = ct
        record.msecs = (ct - int(ct)) * 1000
        return 1

class Sim(object):
    scheduler = scheduler.Scheduler()

    @classmethod
    def add_console_logging(cls, module, term_color):
        show_colors = sys.stderr.isatty() and os.environ.get('TERM', 'dumb') != 'dumb'
        if term_color and show_colors:
            fmt = '%(created)f ' + term_color + '%(message)s' + TERM_COLOR_RESET
        else:
            fmt = '%(created)f %(message)s'
        logger = logging.getLogger(module)
        logger.setLevel(logging.WARNING)
        logger.propagate = 0
        ch = logging.StreamHandler()
        ch.setFormatter(logging.Formatter(fmt=fmt))
        ch.addFilter(SimTimeFilter())
        logger.addHandler(ch)

    @classmethod
    def add_file_logging(cls, module, filename):
        logger = logging.getLogger(module)
        logger.setLevel(logging.WARNING)
        logger.propagate = 0
        if filename == '-':
            fh = logging.StreamHandler(sys.stdout)
        else:
            fh = logging.FileHandler(filename, mode='w', delay=1)
        fh.setFormatter(logging.Formatter(fmt='%(message)s'))
        fh.addFilter(SimTimeFilter())
        logger.addHandler(fh)

    @classmethod
    def init_logging(cls):
        cls.add_console_logging(None, None)
        logging.getLogger().setLevel(logging.DEBUG)

        cls.add_console_logging('bene.link', TERM_COLOR_CYAN)
        cls.add_console_logging('bene.node', TERM_COLOR_MAGENTA)
        cls.add_console_logging('bene.tcp', TERM_COLOR_RED)
        cls.add_console_logging('bene.tcp.sender', TERM_COLOR_YELLOW)
        cls.add_console_logging('bene.tcp.receiver', TERM_COLOR_BLUE)

        cls.add_file_logging('bene.link.queue', 'queue.csv')
        cls.add_file_logging('bene.tcp.sequence', 'sequence.csv')
        cls.add_file_logging('bene.tcp.cwnd', 'cwnd.csv')
