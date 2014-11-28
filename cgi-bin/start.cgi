#!/usr/bin/env python

import cgitb; cgitb.enable()
import os, cgi, sys, operator
from settings import PROJECT_PATH, PROJECT_URL, EDITOR_URL, SAMPLE_PROJECT_PATH
from urlparse import urljoin
from urllib import urlencode
from project import Project
from uuid import uuid1
from shutil import copytree


method = os.environ.get("REQUEST_METHOD", "")

def redirect (url):
    print """Content-type: text/html; charset=utf-8"""
    print
    print """<!DOCTYPE html>
<body style="margin:2em" >
<a id="next" href="{0}">continue</a>
</body>
<script>
var href = document.getElementById("next").getAttribute("href");
window.location = href;
</script>
""".format(url)

errormsg = ""
if method == "POST":
    fs = cgi.FieldStorage()
    project = uuid1().hex
    projpath = os.path.join(PROJECT_PATH, project)
    try:
        copytree(SAMPLE_PROJECT_PATH, projpath)
        proj = Project(project, create=True)
        redirect("{0}?{1}".format(EDITOR_URL, urlencode({'p': proj.path})))
        sys.exit(0)
    except OSError, e:
        errormsg = """An error occurred, check your project name (try without using special characters)<br>\n<div class="error">({0})</div>""".format(e)

projects = []
for p in os.listdir(PROJECT_PATH):
    fp = os.path.join(PROJECT_PATH, p)
    if os.path.isdir(fp) and not p.startswith("."):
        projects.append(Project(p))
projects.sort(key=operator.attrgetter("path"))


print "Content-type:text/html;charset=utf-8"
print
print """
<!DOCTYPE html>
<html>
<head>
<title>Hybrid Publishing Editor</title>
<link rel="stylesheet" type="text/css" href="/editor.css">
</head>
<body style="margin: 2em">
<h1>Hybrid Publishing Editor</h1>
"""
if len(errormsg):
    print """<p class="error">{0}</p>""".format(errormsg).encode("utf-8")
print """
<p>Click the start project button below to start a new project.</p>
<form method="post">
<input type="submit" value="create" />
</form>

</body>
</html>
"""