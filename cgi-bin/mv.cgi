#!/usr/bin/env python

import cgitb; cgitb.enable()
import os, sys, cgi, json
from subprocess import PIPE, Popen
from settings import PROJECT_PATH, PROJECT_URL, EDITOR_URL, MAKE
from project import Project

method = os.environ.get("REQUEST_METHOD", "")
fs = cgi.FieldStorage()
project = fs.getvalue("p", "")
frompaths = fs.getlist("f[]")
topaths = fs.getlist("t[]")

ret = {}
ret['returncode'] = -1

print >> sys.stderr, "mv", frompaths, topaths

passes = 0
fails = 0

if frompaths:
    proj = Project(project)
    for f, t in zip(frompaths, topaths):
        frompath = os.path.join(proj.fullpath, f)
        topath = os.path.join(proj.fullpath, t)
        try:
            os.rename(frompath, topath)
            passes += 1
        except OSError:
            fails += 1
            pass
        # print >> sys.stderr, "***", frompath, topath
    ret['passes'] = passes
    ret['fails'] = fails
    ret['returncode'] = 0

print "Content-type: application/json"
print
print json.dumps(ret)
