#!/usr/bin/env python

import cgitb; cgitb.enable()
import os, cgi, sys, operator
from settings import PROJECT_PATH, PROJECT_URL, EDITOR_URL
from urlparse import urljoin
from urllib import urlencode
from project import Project


method = os.environ.get("REQUEST_METHOD", "")

def redirect (url):
    print """Content-type: text/html; charset=utf-8"""
    print
    print """<!DOCTYPE html>
<body>
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
    project = fs.getvalue("p", "").strip()
    if len(project):
        try:
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
<h1>step 1.</h1>
"""
if len(errormsg):
    print """<p class="error">{0}</p>""".format(errormsg).encode("utf-8")

if len(projects):
    print """<p>Select a project:</p>"""
print """<ul>"""
for p in projects:
    print """<li><a href="{0}?{1}">{2}</a></li>""".format(EDITOR_URL, urlencode({'p': p.path}), p.path)
print """</ul>"""
if len(projects):
    print """<p>or<p>"""
print """
<p>Create a new project folder</p>
<form method="post">
<input type="text" name="p" value="" placeholder="new project folder name" />
<input type="submit" value="create" />
</form>

</body>
</html>
"""