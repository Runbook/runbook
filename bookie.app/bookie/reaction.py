import logging

from .reaction_scaffold import ReactionScaffold

from cliff.command import Command


class Reaction(Command):
    "Generates a new Reaction scaffold, named <reaction> using model <model>."
    
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(Reaction, self).get_parser(prog_name)
        parser.add_argument('reaction', nargs='?', default='')
        return parser

    def take_action(self, parsed_args):
        reaction = parsed_args.reaction
        
        if reaction == '':
            raise RuntimeError('Cannot create a new reaction without a reaction model')

        self.log.info('Creating new reaction "' + reaction + '"')

        self.app.stdout.write('Reaction processing...\n')
        
        scaf = ReactionScaffold(self.log)

        ret = scaf.generate(reaction)


        
