#!/usr/bin/env python

import cgitb; cgitb.enable()
import os, sys, cgi, json
from subprocess import PIPE, Popen
from settings import PROJECT_PATH, PROJECT_URL, EDITOR_URL, MAKE
from project import Project

method = os.environ.get("REQUEST_METHOD", "")
fs = cgi.FieldStorage()
project = fs.getvalue("p", "")
paths = fs.getlist("f[]")

ret = {}
ret['stdout'] = ''
ret['stderr'] = ''
ret['returncode'] = -1

if paths:
    proj = Project(project)
    for p in paths:
        fp = os.path.join(proj.fullpath, p)
        print >> sys.stderr, "*** rm", fp
        os.remove(fp)
    ret['returncode'] = 0

print "Content-type: application/json"
print
print json.dumps(ret)
