#!/usr/bin/env python

import cgitb; cgitb.enable()
import os, sys, cgi
from project import Project
from zipfile import ZipFile 


method = os.environ.get("REQUEST_METHOD", "")
fs = cgi.FieldStorage()
project = fs.getvalue("p", "")
paths = fs.getlist("f[]")

if paths:
    proj = Project(project)
    zippath = os.path.join(proj.fullpath, "{0}.zip".format(project))
    with ZipFile(zippath, 'w') as zzip:
        for p in paths:
            fp = os.path.join(proj.fullpath, p)
            # print >> sys.stderr, "*** rm", fp
            _, base = os.path.split(fp)
            zzip.write(fp, project+"/"+base)
    # serve zippath
    print "Content-type: application/zip"
    print "Content-disposition: attachment; filename={0}.zip".format(project)
    print "Content-length: {0}".format(os.path.getsize(zippath))
    print
    with open(zippath) as f:
        while True:
            data = f.read()
            if data == "":
                break
            sys.stdout.write(data)
    os.unlink(zippath)

