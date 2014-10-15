#!/usr/bin/python
######################################################################
# Generate static HTML for non dynamic pages
######################################################################
# Benjamin J. Cane - 01/02/2014

import jinja2
import os
import codecs


def createFile(path, filename, output):
    ''' Generic Function to Create and write a file '''
    if not os.path.isdir(path):
        os.makedirs(path)

    fh = codecs.open(filename, encoding="utf-8", mode="w")
    fh.write(output)
    fh.close()


def GenStaticPage(f, data, output_dir):
    ''' Create Static Pages '''
    templateLoader = jinja2.FileSystemLoader(searchpath="./templates/")
    templateEnv = jinja2.Environment(loader=templateLoader)
    template = templateEnv.get_template(f)
    tempVars = {'data': data}
    outputText = template.render(tempVars)
    outputText.encode('utf-8')
    # Create the page
    filedir = output_dir + "/" + data['url']
    filename = output_dir + "/" + data['url'] + "/index.html"
    createFile(filedir, filename, outputText)

    return True

out_path = "/data/crstatic/public_html/"
pages = {
    "/": "index-2.html",
    "/monitors": "monitors.html",
    "/reactions": "reactions.html",
    "/tos": "tos.html"
}

for key in pages.keys():
    data = {}
    data['url'] = key
    data['active'] = key
    data['loggedin'] = False

    if GenStaticPage(pages[key], data, out_path):
        print("Successfully created %s") % key
    else:
        print("Did not create %s") % key
