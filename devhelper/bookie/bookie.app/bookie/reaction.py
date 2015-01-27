import logging

from .reaction_scaffold import ReactionScaffold

from cliff.command import Command


class Reaction(Command):
    "Generates a new Reaction scaffold using model file."
    
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(Reaction, self).get_parser(prog_name)
        parser.add_argument('--force-overwrite', '-f', action='store_true')
        parser.add_argument('model', nargs='?', default='')
        return parser

    def take_action(self, parsed_args):
        model = parsed_args.model
        force_overwrite = parsed_args.force_overwrite

        if model == '':
            raise RuntimeError('Cannot create a new reaction without a reaction model')

        self.log.debug('reaction processing started...\n')
        
        scaf = ReactionScaffold(self.log, model, force_overwrite)

        ret = scaf.generate()

        self.log.debug('reaction processing done.\n')

        if ret == True:
            self.log.info('successfully created scaffolding for reaction templates from model "' + model + '"')
        else:
            self.log.info('scaffolding for reaction from model "' + model + '" failed!')
        
        
        
