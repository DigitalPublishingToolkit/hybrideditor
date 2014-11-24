#!/usr/bin/env python

import cgitb; cgitb.enable()
import os, sys, cgi, mimetypes
from settings import PROJECT_PATH, PROJECT_URL, EDITOR_URL
from project import Project
from urlparse import urljoin
from urllib import urlencode


print """Content-type: text/html; charset=utf-8"""
print

method = os.environ.get("REQUEST_METHOD", "")
fs = cgi.FieldStorage()
project = fs.getvalue("p", "")
proj = Project(project)
varz = {}
varz['project'] = proj.path
varz['listing_url'] = "/cgi-bin/listing.cgi?"+urlencode({'p': proj.path})
varz['make_url'] = "/cgi-bin/make.cgi?"+urlencode({'p': proj.path})
varz['rm_url'] = "/cgi-bin/rm.cgi?"+urlencode({'p': proj.path})
varz['save_url'] = "/cgi-bin/save.cgi?"+urlencode({'p': proj.path})

print """<!DOCTYPE html>
<html>
<head>
<title>hype : {0[project]}</title>
<link rel="stylesheet" type="text/css" href="/lib/jquery-ui/jquery-ui.min.css"></script>
<link rel="stylesheet" type="text/css" href="/editor.css">
<link rel="listing-data-source" href="{0[listing_url]}">
<link rel="make-url" href="{0[make_url]}">
<link rel="rm-url" href="{0[rm_url]}">
<link rel="save-url" href="{0[save_url]}">
</head>
<body>
<div id="contents">
    <div id="split" class="frame">
        <div id="listing" class="left">
            <div class="controls">
                <span class="selection_functions">
                    <button id="listing_delete_selection">delete selected</button>
                </span>
                <button id="listing_select_all">select all</button>
                <button id="listing_refresh_button" class="refresh">refresh</button>
            </div>
            <div class="body"></div>
        </div>
        <div class="hdiv"></div>
        <div id="editor" class="right"></div>
    </div>

    <div id="footer"><a href="https://github.com/DigitalPublishingToolkit/hybrideditor">Hybrid Publishing Editor</a> is <a href="http://www.gnu.org/copyleft/gpl.html">free software</a> based on <a href="http://www.gnu.org/software/make/">make</a>, <a href="http://johnmacfarlane.net/pandoc/">pandoc</a>, <a href="http://daringfireball.net/projects/markdown/">markdown</a>, &amp; <a href="http://ace.c9.io/">ace</a>.
        <a href="http://networkcultures.org/digitalpublishing/"><img src="/imgs/logo_horiz.jpg" class="logo" alt="" ></a>
    </div>

</div>
</body>
<script>
aa = {{}};
</script>
<script src="/lib/jquery.min.js"></script>
<script src="/lib/jquery.nicescroll.min.js"></script>
<script src="/lib/jquery-ui/jquery-ui.min.js"></script>
<script src="/lib/d3.min.js"></script>
<script src="/lib/dropzone/dropzone.js"></script>
<script src="/lib/ace-builds/src/ace.js" type="text/javascript" charset="utf-8"></script>
<script src="/lib/aa/frames.js"></script>
<script src="/lib/aa/ace-modelist.js"></script>
<script src="/lib/aa/ace-editor.js"></script>
<script src="/lib/mediafragments.js"></script>
<script src="/lib/aa/href.js"></script>
<script src="/editor.js"></script>
</html>
""".format(varz)






