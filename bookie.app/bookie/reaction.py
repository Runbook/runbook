import logging

from .reaction_scaffold import ReactionScaffold

from cliff.command import Command


class Reaction(Command):
    "Generates a new Reaction scaffold, named <reaction> using model <model>."
    
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(Reaction, self).get_parser(prog_name)
        parser.add_argument('reaction', nargs='?', default='')
        parser.add_argument('model', nargs='?', default='')
        return parser

    def take_action(self, parsed_args):
        reaction = parsed_args.reaction
        model = parsed_args.model
        
        if reaction == '' or model == '':
            raise RuntimeError('Cannot create a new reaction with an empty name/model')

        self.log.info('Creating new reaction "' + reaction + '" with reference "' + model + '"')

        self.app.stdout.write('Reaction processing...\n')
        
        scaf = ReactionScaffold(self.log)

        ret = scaf.generate(reaction, model)


        
