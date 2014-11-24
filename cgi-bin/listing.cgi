#!/usr/bin/env python

import cgitb; cgitb.enable()
import os, sys, cgi, json
from project import Project


fs = cgi.FieldStorage()
project = fs.getvalue("p", "")
proj = Project(project)

print "Content-Type: application/json"
print
print json.dumps(proj._dict())
sys.exit(0)

# varz = {}
# varz['project'] = project
# varz['json_url'] = "?" + urlencode({'project': proj.path, 'format': 'json'})

# print """Content-Type: text/html; charset=utf-8"""
# print
# print """<!DOCTYPE html>
# <html>
# <head>
# <title>hybrid editor: {0[project]}</title>
# <link rel="data-source" href="{0[json_url]}">
# <link rel="stylesheet" type="text/css" href="/listing.css">
# </head>
# <body>

# </body>
# <script src="/lib/d3.min.js"></script>
# <script src="/listing.js"></script>
# </html>
# """.format(varz)






