#!/usr/bin/env python

import cgitb; cgitb.enable()
import os, sys, cgi, json
from subprocess import PIPE, Popen
from settings import PROJECT_PATH, PROJECT_URL, EDITOR_URL, MAKE
from project import Project
from time import sleep

method = os.environ.get("REQUEST_METHOD", "")
fs = cgi.FieldStorage()
project = fs.getvalue("p", "")
paths = fs.getlist("f[]")

ret = {}
passes = 0
fails = 0

proj = Project(project)
if len(paths) == 0:
    count = 1
    newname = "untitled_file.md"
    fp = os.path.join(proj.fullpath, newname)
    while os.path.exists(fp):
        count += 1
        newname = "untitled_file_{0}.md".format(count)
        fp = os.path.join(proj.fullpath, newname)
        sleep(0.001)

    args = ["touch", fp]
    p = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE, cwd=proj.fullpath)
    stdout, stderr = p.communicate()
    if p.returncode == 0:
        passes += 1
    else:
        fails += 1
else:
    for p in paths:
        fp = os.path.join(proj.fullpath, p)

        # print >> sys.stderr, "*** rm", fp
        try:
            args = ["touch", fp]
            p = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE, cwd=proj.fullpath)
            stdout, stderr = p.communicate()
            if p.returncode == 0:
                passes += 1
            else:
                fails += 1
        except OSError, e:
            fails += 1

ret['passes'] = passes
ret['fails'] = fails

print "Content-type: application/json"
print
print json.dumps(ret)
