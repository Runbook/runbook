#!/bin/python
#####################################################################
# Post Classes
#####################################################################

import yaml
import re
import markdown


class Post:

    ''' This is a class used to define posts '''

    def __init__(self, metadata, postdata):
        ''' Initialize a Post Object '''
        self.metadata = metadata
        self.postdata = postdata
        self.parseMetaData(self.metadata)
        self.generatePostHTML(self.postdata)

        # Set some variables that will be set later
        self.nextp = None
        self.prevp = None

    def to_unicode_or_bust(obj, encoding='utf-8'):
        if isinstance(obj, basestring):
            if not isinstance(obj, unicode):
                obj = unicode(obj, encoding)
        return obj

    def parseMetaData(self, metadata):
        ''' Parse Post Meta Data and set self variables '''
        meta = yaml.safe_load(metadata)

        # Date Information
        data = str(meta['date']).split()
        ymd = data[0].split("-")
        self.year = ymd[0]
        self.month = ymd[1]
        self.day = ymd[2]
        self.date = self.year + "/" + self.month + "/" + self.day

        self.pubdate = None
        if "pubdate" in meta:
            self.pubdate = meta['pubdate']

        self.pid = meta['post_id']
        self.slug = meta['slug']
        self.title = meta['title']
        self.author = meta['author']
        self.authorlink = meta['authorlink']
        self.cats = meta['categories']
        self.tags = meta['tags']
        self.popularity = None
        if meta['popularity'] is True:
            self.popularity = True

        if "description" in meta:
            self.description = meta['description']
        else:
            self.description = None
        if "thumbnail" in meta:
            self.thumbnail = meta['thumbnail']
        else:
            self.thumbnail = None

        # Generate Page URL
        self.url = "/" + self.date + "/" + self.slug
        self.url2 = "/" + self.year + "/" + self.month + "/" + self.slug

    def generatePostHTML(self, data):
        ''' Generates HTML Data from markdown version of blog post '''
        mdcon = markdown.Markdown(extensions=["toc"])
        html = mdcon.convert(data)
        self.posthtml = html
        temptoc = mdcon.toc

        #unitoc = self.to_unicode_or_bust(temptoc)
        # unitoc.decode('utf-8')

        # Create a TOC list of only H2 and H3 Headers
        toc = ""
        toccount = 0
        linktxt = u'<li class="list-group-item"><a href="%s">%s</a></li>\n'
        for x in temptoc.split("\n"):
            y = x.encode("utf-8")
            reg = re.search('="(.+?)">(.+?)<', y)
            if reg:
                f1 = reg.group(1)
                f2 = reg.group(2)
                newline = linktxt % (f1, f2)
                toc = toc + newline
                toccount = toccount + 1

        self.tochtml = toc
        self.toccount = toccount
