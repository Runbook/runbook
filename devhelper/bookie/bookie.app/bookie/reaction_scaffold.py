import os
import re

from jinja2 import Template

import yaml

# if CLoader/CDumper are available (i.e. user has libyaml installed)
#  then use them since they are much faster.
optimized_yaml=False
try:
    from yaml import CLoader as Loader
    from yaml import CDumper as Dumper
    optimized_yaml=True
except ImportError:
    from yaml import Loader
    from yaml import Dumper

from .resources import Models
from .helper import mkdir_p

class ReactionScaffold:

    def __init__(self, logger, filename, force_overwrite=False):
        self.log = logger
        self.filename = filename
        self.force_overwrite = force_overwrite

        self.log.debug("Optimized libyaml: %s" % optimized_yaml)

        stream = file(filename, 'r')
        self.data = yaml.load(stream)

        self.reaction = self.data['reaction']['name']

        self.vclasses = set()
        self.tclasses = set()
        
        self.has_call_on = False
        
        for attr in self.data['attributes']:
            attribute=attr['attribute']
            if attribute != 'call_on':
                name=attr['name']
                desc=attr['desc']
                
                type=attr['type']
                self.tclasses.add(type)
                
                validators=attr['validators']
                for v in validators:
                    vclass=re.sub("([^\(]*).*",r"\1", v)
                    self.vclasses.add(vclass)
                else:
                    self.has_call_on = True
                    self.tclasses.add('SelectField')
                    self.vclasses.add('DataRequired')
        
        
        

    def can_write(self, filename):
        self.log.debug("checking filename: %s" % filename)
        return self.force_overwrite or not os.path.exists(filename)


    def generate(self):        
        name=self.data['reaction']['name']
        
        self.log.debug("got name %s" % name)

        self.generate_model()
        self.generate_view()
        self.generate_controller()

        return True


    def generate_model(self):
        basedir='src/web/reactionforms/%s' % self.reaction
        
        filename='%s/__init__.py' % basedir
        
        if self.can_write(filename):
            mkdir_p(basedir)
            f = open(filename, 'w')
            template_file = Models.model_template()

            template = Template(template_file)
            output = template.render({"data":self.data, "vclasses": self.vclasses, "tclasses":self.tclasses, "has_call_on":self.has_call_on} )

            f.write(output)
            
        return True

    def generate_view(self):
        reaction=self.data['reaction']['name']
        
        basedir='src/web/templates/reactions'
        html_filename = '%s/%s.html' % (basedir, reaction)
        js_filename = '%s/%s.js' % (basedir, reaction)

        if self.can_write(html_filename):
            mkdir_p(basedir)
            f = open(html_filename, 'w')
            template_file = Models.view_template()

            template = Template(template_file)
            output = template.render({"data":self.data, "vclasses": self.vclasses, "tclasses":self.tclasses, "has_call_on":self.has_call_on} )

            f.write(output)

        return True


    def generate_controller(self):
        basedir='src/actions/actions/%s' % self.reaction
        
        filename='%s/__init__.py' % basedir
        
        if self.can_write(filename):
            mkdir_p(basedir)
            f = open(filename, 'w')
            template_file = Models.controller_template()

            template = Template(template_file)
            output = template.render({"data":self.data, "vclasses": self.vclasses, "tclasses":self.tclasses, "has_call_on":self.has_call_on} )

            f.write(output)

        return True

