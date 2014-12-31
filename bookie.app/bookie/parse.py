#!/usr/bin/env python

import os
import sys
import errno
import re
import yaml
from jinja2 import Template

from yaml import CLoader, CDumper
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

print "Optimized libyaml: %s" % optimized_yaml



def f3():
    data=yaml.load(stream)

    print reaction

    print title

    for attr in data['attributes']:
        attribute=attr['attribute']
        if attribute != 'call_on':
            type=attr['type']
            name=attr['name']
            desc=attr['desc']
            validators=attr['validators']

        print '%s | %s | %s | %s | %s |' % (attribute, type, name, desc, validators)


# Thanks to tzot ( http://stackoverflow.com/questions/600268/mkdir-p-functionality-in-python )
def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise


class Models:
    @staticmethod
    def model_template():
        return open("templates/model.jinja", 'r').read()

    def view_template():
        return open("templates/view.jinja", 'r').read()

    def controller_template():
        return


class ReactionScaffold:

    def __init__(self, filename, force_overwrite=False):
        self.filename = filename
        self.force_overwrite = force_overwrite

        stream = file(filename, 'r')
        self.data = yaml.load(stream)

        self.reaction = self.data['reaction']['name']


    def can_write(self, filename):
        print "checking filename: %s" % filename
        return self.force_overwrite or not os.path.exists(filename)


    def generate(self):        
        name=self.data['reaction']['name']
        
        print "got name %s" % name

        self.generate_model()
        self.generate_view()
#        self.generate_controller(data)

        return True


    def generate_model(self):
        basedir='src/web/reactionforms/%s' % self.reaction
        
        filename='%s/__init__.py' % basedir
        
        if self.can_write(filename):
            vclasses = set()
            tclasses = set()
            
            has_call_on = False

	    for attr in self.data['attributes']:
	        attribute=attr['attribute']
	        if attribute != 'call_on':
	            name=attr['name']
	            desc=attr['desc']

	            type=attr['type']
                    tclasses.add(type)

	            validators=attr['validators']
                    for v in validators:
                        vclass=re.sub("([^\(]*).*",r"\1", v)
                        vclasses.add(vclass)
                else:
                    has_call_on = True
                    tclasses.add('SelectField')
                    vclasses.add('DataRequired')
	
#                print '%s | %s | %s | %s | %s |' % (attribute, type, name, desc, validators)

            mkdir_p(basedir)
            f = open(filename, 'w')
            template_file = Models.model_template()

#            print "template = %s" % template_file

            template = Template(template_file)
            output = template.render({"data":self.data, "vclasses": vclasses, "tclasses":tclasses, "has_call_on":has_call_on} )

#            print("=====data: %s" % self.data)
	
#            print("validators : %s" % vclasses)
#            print("types : %s" % tclasses)
            f.write(output)
            

        return True

    def generate_view(self):
        reaction=self.data['reaction']['name']
        
        basedir='src/web/reactionforms/%s' % reaction
        
        filename='%s/__init__.py' % basedir
        
        if self.can_write(filename):
            print

            
r=ReactionScaffold(sys.argv[1], True)

r.generate()

exit(0)
