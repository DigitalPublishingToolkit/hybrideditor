#!/usr/bin/env python

import cgitb; cgitb.enable()
import cgi, os, sys, json
from project import Project


fs =cgi.FieldStorage()
project = fs.getvalue("p", "")
proj = Project(project)
method = os.environ.get("REQUEST_METHOD")

# print "Hello", method
# cgi.print_environ()

UPLOADS = "/home/murtaugh/projects/DPT/hybrideditor/projects/uploads/"

def upload (form, inputname, upload_dir):
    if not form.has_key(inputname): return
    fileitems = form[inputname]
    if not isinstance(fileitems, list):
        fileitems = [fileitems]
    ret = []
    for fileitem in fileitems:
        if not fileitem.file:
            continue
        if not fileitem.filename:
            continue
        fp = os.path.join(upload_dir, fileitem.filename)
        fout = file (fp, 'wb')
        bytes = 0
        while 1:
            chunk = fileitem.file.read(100000)
            if not chunk: break
            bytes += len(chunk)
            fout.write (chunk)
        fout.close()
        ret.append((fileitem.filename, bytes))
    return ret

if method == "POST":
    result = upload(fs, "files[]", proj.fullpath)
    if result:
        print "Content-type: application/json"
        print ""
        print json.dumps(result)
        sys.exit(0)

        # for filename, bytes in result:
        #     print "{0} bytes written to {1}<br />".format(bytes, filename)
    else:
        print "Content-type:text/html;charset=utf-8"
        print
        print "No upload"
    print "<a href="">upload another</a>"
else:

    print "Content-type:text/html;charset=utf-8"
    print
    print """<!DOCTYPE html>
<html>
<head>
</head>
<body>
<form method="post" action="" enctype="multipart/form-data">
<input type="file" name="file[]" multiple><input type="submit">
<input type="hidden" name="p" value="{0}>
</form>
</body>
</html>
""".format(project)