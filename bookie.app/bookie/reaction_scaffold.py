import collections
import yaml

# if CLoader/CDumper are available (i.e. user has libyaml installed)
#  then use them since they are much faster.
try:
    from yaml import CLoader as Loader
    from yaml import CDumper as Dumper
except ImportError:
    from yaml import Loader
    from yaml import Dumper


class ReactionScaffold:

    def __init__(self, logger):
        self.log = logger

    def generate(self, reaction, model):
        ret = collections.namedtuple('Return', ['status', 'logs'])
        status = 0
        logs = ['line 1', 'line 2']


        self.log.info("reaction generator returned {d}".format(d=status))

        for l in logs:
            self.log.info(l)

        return True


#for data in yaml.load_all(documents):
#    print data
