#!/usr/bin/env python

import cgitb; cgitb.enable()
import cgi, os, sys, subprocess
from tempfile import NamedTemporaryFile as NTF 
from settings import PANDOC 


"""

Simple Upload form that saves files to a temp named file,
calls pandoc for conversion to a given format,
& displays results in browser.

Uses a temp file because formats like docx are considered "archives"
and need to be accessed by pandoc as filenames to actual filenames
(not piped directly in)

"""

method = os.environ.get("REQUEST_METHOD")
_types = {
    'markdown': { 'mime': "text/plain;charset=utf-8", 'ext': 'markdown' },
    # 'icml': { 'mime': "application/xml;charset=utf-8", 'ext': 'icml' },
    'icml': { 'mime': "text/plain;charset=utf-8", 'ext': 'icml' },
    'docx': { 'mime': "application/vnd.openxmlformats-officedocument.wordprocessingml.document;charset=utf-8", 'ext': 'docx' },
    'html': { 'mime': "text/html;charset=utf-8", 'ext': 'html' }
}
DEFAULT_TYPE = { 'mime': "text/plain;charset=utf-8", 'ext': 'txt' }

def guess_format_from_filename (fn):
    if fn.endswith(".docx"):
        return "docx"
    return "txt"

if method == "POST":
    fs = cgi.FieldStorage()
    from_format = fs.getvalue("from")
    to_format = fs.getvalue("to", "markdown")
    to_type = _types.get(to_format, DEFAULT_TYPE)
    submit = fs.getvalue("_submit", "submit")
    download = submit == "download"
    download_filename = None
    if download:
        download_filename = "pandoc" + to_type['ext']


    try:
        f = fs["file"]
    except KeyError:
        f = None
    ###################################
    # FILE INPUT
    ###################################
    if f != None and f.file:

        if from_format == None:
            from_format = guess_format_from_filename(f.filename)

        tmp = NTF(delete=False)
        bytes = 0
        while True:
            data = f.file.read()
            if not data:
                break
            bytes += len(data)
            tmp.write(data)
        # print "saved to '{0}'<br>".format(tmp.name)
        # print "read {0} bytes<br>".format(bytes)
        tmp.close()
        try:

            print "Content-type: {0}".format(to_type['mime'])
            if download:
                print "Content-Disposition: attachment;filename=\"pandoc.{0}\"".format(to_type['ext'])
            print
            # p = subprocess.check_output('pandoc --from {0} --to {1} "{2}"'.format(ffrom, to, tmp.name), shell=True, stderr=subprocess.STDOUT)
            # print p
            p = subprocess.Popen([PANDOC, '--from', from_format, '--to', to_format, tmp.name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            out, err = p.communicate()
            print out

        except subprocess.CalledProcessError, e:
            print "Content-type: text/html;charset=utf-8"
            print
            print u"<span style='font-family:monospace'>An error occurred, pandoc said: {0}</span>".format(e.output).format("utf-8")

        tmp.unlink(tmp.name)

    ###################################
    # FORM/TEXT INPUT
    ###################################
    else:
        text = fs.getvalue("text")
        if from_format and to_format:
            try:
                print "Content-type: {0}".format(to_type['mime'])
                if download:
                    print "Content-Disposition: attachment;filename=\"pandoc.{0}\"".format(to_type['ext'])
                print
                # p = subprocess.check_output('pandoc --from {0} --to {1} "{2}"'.format(ffrom, to, tmp.name), shell=True, stderr=subprocess.STDOUT)
                # print p
                p = subprocess.Popen([PANDOC, '--from', from_format, '--to', to_format], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                out, err = p.communicate(text)
                print out

            except subprocess.CalledProcessError, e:
                print "Content-type: text/html;charset=utf-8"
                print
                print u"<span style='font-family:monospace'>An error occurred, pandoc said: {0}</span>".format(e.output).encode("utf-8")

        else:
            print "Content-type: text/html;charset=utf-8"
            print
            print u"<span style='font-family:monospace'>Format unspecified</span>".encode("utf-8")

    sys.exit(0)

print "Content-type: text/html;charset=utf-8"
print
print """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8" />
</head>
<body>
<form enctype="multipart/form-data" action="" method="post">
<p>Convert: <input type="file" name="file"></p>
to: <select name="to">
    <option>markdown</option>
    <option>html</option>
</select>
<p><input type="submit" value="OK"></p>
</form>
</body></html>
"""