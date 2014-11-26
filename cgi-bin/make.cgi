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
dryrun = fs.getvalue("n", "")

if path:
    proj = Project(project)
    if dryrun:
        p = Popen([MAKE, "-n", path], stdin=PIPE, stdout=PIPE, stderr=PIPE, cwd=proj.fullpath)
    else:
        p = Popen([MAKE, path], stdin=PIPE, stdout=PIPE, stderr=PIPE, cwd=proj.fullpath)
    stdout, stderr = p.communicate()
    ret = {}
    ret['stdout'] = stdout
    ret['stderr'] = stderr
    ret['returncode'] = p.returncode

    print "Content-type: application/json"
    print
    print json.dumps(ret)
