#!/usr/bin/env python

import cgitb; cgitb.enable()
import os, sys, cgi, json
from subprocess import PIPE, Popen
from settings import PROJECT_PATH, PROJECT_URL, EDITOR_URL, MAKE
from project import Project

method = os.environ.get("REQUEST_METHOD", "")
fs = cgi.FieldStorage()
project = fs.getvalue("p", "")
path = fs.getvalue("f")
content = fs.getvalue("text")

ret = {}
ret['returncode'] = -1

if path and content != None:
    proj = Project(project)
    fp = os.path.join(proj.fullpath, path)
    with open(fp, "w") as f:
        f.write(content)
    ret['returncode'] = 0

print "Content-type: application/json"
print
print json.dumps(ret)
