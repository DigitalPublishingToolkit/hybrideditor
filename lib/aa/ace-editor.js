/*

(C) 2014 Michael Murtaugh and Active Archives contributors
This software is part of Active Archives
http://activearchives.org/
Released under a GPL3 license.
Please include this message when redistributing.
Requires: Ace

*/

function aa_aceeditor (ace) {
    ace = ace || window.ace;
    var factory = {name: 'aceeditor'},
        sessionsByHref = {},
	    modelist = ace.require("ace/ext/modelist");

    factory.get_session = function (href) {
        return sessionsByHref[href];
    }

    // editor.get_element ()
    factory.get_editor = function () {
        var editor = { factory: factory },
            tokenclicks,
            current_href,
            highlightLineStart,
            highlightLineEnd,
            _save;

        editor.elt = document.createElement("div");

        var root = d3.select(editor.elt)
                .attr("class", "editor"),
            body = root.append("div")
                .attr("class", "editorbody"),
            foot = root.append("div")
                .attr("class", "editorfoot");

        editor.aceeditor = ace.edit(body[0][0]);

        editor.save = function (callback) {
            _save = callback;
        }

        // a bit of a brutal solution but...
        $(document).bind("resize", function (e) {
            // console.log("ace.resize");
            editor.aceeditor.resize();
        });

	    // MODE SELECTOR
        var modeselector = foot
            .append("select")
            .attr("class", "editormode");

	    modeselector
	        .on("change", function () {
	            // console.log("change", this, this.value);
	            editor.aceeditor.getSession().setMode(this.value);
	        })
	        .selectAll("option")
	        .data(modelist.modes)
	        .enter()
	        .append("option")
	        .attr("value", function (d) { return d.mode; })
	        .text(function (d) { return d.caption; });

        var save = foot
            .append("button")
            .text("save")
            .on("click", function () {
                var text = editor.aceeditor.getValue();
                if (_save) {
                    _save.call(editor, {
                        text: text,
                        href: current_href
                    });
                }
            });

        function highlight(s, e) {
            var session = editor.aceeditor.getSession();
            if (highlightLineStart) {
                for (var i=(highlightLineStart-1); i<=(highlightLineEnd-1); i++) {
                    session.removeGutterDecoration(i, 'ace_gutter_active_annotation');
                }
            }
            highlightLineStart = s;
            highlightLineEnd = e;
            if (highlightLineStart) {
                for (var i=(highlightLineStart-1); i<=(highlightLineEnd-1); i++) {
                    session.addGutterDecoration(i, 'ace_gutter_active_annotation');
                }
                editor.aceeditor.scrollToLine(highlightLineStart, true, true);
            }
        }

        editor.href = function (href, done, forceReload) {
            if (arguments.length == 0) {
                var ret = current_href;
                if (highlightLineStart) {
                    ret = aa.lineRangeHref(current_href, highlightLineStart, highlightLineEnd);
                }
                return ret;
            }
            var href = aa.href(href),
                session = sessionsByHref[href.nofrag];
            current_href = href.nofrag;

            if (session == "loading") {
                return false;
            }
            /*
            todo, improve this.. now commented out to force reload
            if (session != undefined) {
                if (done) {
                    window.setTimeout(function () {
                        done.call(session);
                    }, 0);
                }
                editor.aceeditor.setSession(session.acesession);
                // deal with eventual changed fragment
                if (href.lineStart) {
                    highlight(href.lineStart, href.lineEnd);
                    $(editor.elt).trigger("fragmentupdate", {editor: editor});
                }

                return true;
            }
            */
            sessionsByHref[href.nofrag] = "loading";
            $.ajax({
                url: href.nofrag,
                data: { f: (new Date()).getTime() },
                success: function (data) {
                    // console.log("got data", data);
                    var mode = modelist.getModeForPath(href.nofrag).mode || "ace/mode/text",
                        session = { href: href.nofrag, editor: editor };
                    
                    session.acesession = ace.createEditSession(data, mode);
                    // index(href.nofrag, data);
                    modeselector[0][0].value = mode;
                    editor.aceeditor.setSession(session.acesession);
                    // editor.setOption("showLineNumbers", false);
                    editor.aceeditor.setHighlightActiveLine(false);
                    session.acesession.setUseWrapMode(true);
                    sessionsByHref[href.nofrag] = session;
                    if (done) {
                        window.setTimeout(function () {
                            done.call(session);
                        }, 0);
                    }
                },
                error: function (code) {
                    console.log("aceeditor: error loading", href.nofrag, code);
                }
            });
        }

        var observed_href = null;
        $(document).on("fragmentupdate", function (e, data) {
            if ((e.target !== editor.elt) && data.editor) {
                observed_href = data.editor.href();
                // console.log("ace.fragmentupdate", e.target, observed_href);
            }
        });

        editor.newSession = function () {
            var session = ace.createEditSession("", "ace/mode/srt-md");
            editor.aceeditor.setSession(session);
        }


        function bind_keys (e) {
            return;
            /*
            e.commands.addCommand({
                name: 'pasteTimecode',
                bindKey: {win: 'ctrl-shift-down',  mac: 'command-shift-down'},
                exec: function () {
                    if (observed_href) {
                        var href = aa.href(observed_href),
                            mode = editor.aceeditor.getSession().getMode().$id,
                            link;
                        // console.log("pasteTimecode", mode);
                        if (mode == "ace/mode/srtmd") {
                            link = aa.secondsToTimecode(href.start)+" -->\n";
                        } else if (mode == "ace/mode/markdown") {
                            link = "["+href.basename+"]("+href.href+")";
                        } else {
                            link = href.href;
                        }
                        editor.aceeditor.insert(link);

                    }
                },
                readOnly: false
            });
            */
        }
        bind_keys(editor.aceeditor);

        return editor;
    };

    return factory;
};
