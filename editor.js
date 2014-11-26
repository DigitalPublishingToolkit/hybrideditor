var editor_factory = aa_aceeditor(window.ace),
    editor = editor_factory.get_editor(),
    editor_elt = d3.select(editor.elt),
    cgi_url = d3.select("link[rel='cgi-url']").attr("href"),

    preview_div = d3.select("#editor")
        .append("div")
        .attr("class", "preview"),
    preview_iframe = preview_div
        .append("iframe"),

    make_div = d3.select("#editor")
        .append("div")
        .attr("class", "make"),
    make_body = make_div.append("div")
        .attr("class", "body"),
    make_icon = make_div
        .append("div")
        .attr("class", "icon"),
    make_gear = make_icon
        .append("div")
        .attr("class", "gear");

function url_for (script) {
    return cgi_url+script+"?p=" + encodeURIComponent(project);
}

function path_for_href (href) {
    var p = new RegExp("^/projects/([^/]+)/(.*)$"),
        m = href.match(p);
    if (m != null) {
        return m[2];
    }
}

editor.save(function (data) {
    console.log("save", data);
    $.ajax({
        url: url_for("save.cgi"),
        method: "post",
        data: {
            text: data.text,
            f: path_for_href(data.href)
        },
        dataType: "json",
        success: function (data) {
            // console.log("save.success", data);
            refresh_listing();
        },
        error: function (err) {
            console.log("save error", err);
        }
    })
});

make_body
    .append("div")
    .attr("class", "stdout");
make_body
    .append("div")
    .attr("class", "stderr");

make_gear.on("click", toggle_make);

var make_height = 300;

function open_make () {
    var cur_height = parseInt(make_div.style("height"));
    if (cur_height == 0) {
        make_div.style("height", make_height+"px"); 
    }
}

function close_make () {
    var cur_height = parseInt(make_div.style("height"));
    if (cur_height > 0) {
        make_div.style("height", 0); 
    }
}

function toggle_make () {
    var cur_height = parseInt(make_div.style("height"));
    if (cur_height > 0) {
        make_height = cur_height;
        make_div.style("height", 0); 
    } else {
        make_div.style("height", make_height+"px"); 
    }
}

aa_frames(document.getElementById("split"));

document.getElementById("editor").appendChild(editor.elt);

function edit (url) {
    editor.href(url);
    editor_elt
        .style("display", "block");
    preview_div
        .style("display", "none");
    close_make();
    // make_div.style("display", "none");
}

function preview (url) {
    preview_div
        .style("display", "block");
    editor_elt
        .style("display", "none");
    preview_iframe
        .attr("src", url);
    close_make();
    // make_div.style("display", "none");
}

function make (path, done) {
    // console.log("make", path);
    var make_url = url_for("make.cgi");
    make_busy(true);
    open_make();
    make_url += "&f="+encodeURIComponent(path);
    // 1. DRY-RUN TO SEE THE COMMAND THAT *WILL* HAPPEN NEXT
    // (and display it)
    d3.json(make_url+"&n=1", function (data) {
        d3.select("#editor .make .stdout").text(data.stdout);
        d3.select("#editor .make .stderr").text(data.stderr);
        if (data.returncode == 0) {
            // NOW MAKE FOR REAL
            d3.json(make_url, function (data) {
                console.log("make done", data);
                d3.select("#editor .make .stdout").text(data.stdout);
                d3.select("#editor .make .stderr").text(data.stderr);
                if (data.returncode == 0) {
                    close_make();
                }
                make_busy(false);
                refresh_listing(done); // nb done will get called with refresh data, not make data
            });
        }        
    })
}

function make_busy (val) {
    make_div.classed("busy", val);
}
/*
function select_all () {
    var checkboxes = d3.selectAll(".itemcheckbox"),
        checked = d3.selectAll(".itemcheckbox:checked");
    if (checkboxes.size() == checked.size()) {
        checkboxes.property("checked", false);
    } else {
        checkboxes.property("checked", true);
    }
    update_selection();
}
*/

function delete_selection () {
    var items_selected = d3.selectAll("#listing div.selected"),
        num_selected = items_selected.size(),
        paths = items_selected.data().map(function (d) { return d.path });

    if (num_selected == 0) return;
    var ok = confirm("Delete "+num_selected+" selected file"+((num_selected==1)?"":"s") + "?");
    if (ok) {
        $.ajax({
             url: url_for("rm.cgi"),
             method: "post",
             data: {
                 'f[]': paths 
             },
             dataType: "json",
             success: function (data) {
                items_selected.each(item_deselect);
                update_selection();
                // console.log("rm response", data);
                refresh_listing();
             }
        });
    }
}

var longclick_begin;

function item_select (d) {
    var elt = d3.select(this),
        eltwidth = $("a", this).width();
    elt
        .classed("selected", true)
        .select("input.itemcheckbox")
        .property("checked", true);
    if (d.exists) {
        elt
            .append("input")
            .attr("type", "text")
            .attr("class", "rename")
            .property("value", d.path)
            .style("width", eltwidth+"px");
        elt.select("a").classed("rename", true);        
    }
}

function item_deselect (d) {
    var elt = d3.select(this);
    elt
        .classed("selected", false)
        .select("input.itemcheckbox")
        .property("checked", false);
    elt.select("a").classed("rename", false);        
    elt
        .select("input.rename")
        .remove();
}

function checkbox_click (d) {
    var checked = d3.select(this).property("checked");
    if (checked) {
        d3.select(this.parentNode).each(item_select);
    } else {
        d3.select(this.parentNode).each(item_deselect);
    }
    update_selection();
}

function item_longclick(d) {
    d3.select(this.parentNode).each(item_select);
    update_selection();
}

function update_selection() {
    var items_all = d3.selectAll("#listing div.item"),
        items_selected = d3.selectAll("#listing div.selected"),
        numselected = items_selected.size(),
        selfunk = d3.select("#listing .selection_functions"),
        regfunk = d3.select("#listing .regular_functions");
    if (numselected >= 1) {
        selfunk.style("display", "inline");
        regfunk.style("display", "none");
    } else {
        selfunk.style("display", "none");
        regfunk.style("display", "inline")
    }
}

function listing_cancel () {
    d3.selectAll("#listing div.selected").each(item_deselect);
    update_selection();
}

function rename () {
    var ss = d3.selectAll("#listing a.rename"),
        frompaths = [],
        topaths = [];
    if (ss.size() == 0) {
        $("#listing .listing_rename_buttons").hide();
        return;
    }
    var ok = confirm("Rename "+ss.size()+" file"+((ss==1)?"":"s") + "?");
    if (ok) {
        ss.each(function (d) {
            var newpath = d3.select(this.parentNode).select("input.rename").property("value");
            frompaths.push(d.path);
            topaths.push(newpath);
        });
        console.log("data", frompaths, topaths);
        $.ajax({
             url: url_for("mv.cgi"),
             method: "post",
             data: {
                 'f[]': frompaths,
                 't[]': topaths
             },
             dataType: "json",
             success: function (data) {
                // console.log("success", data);
                listing_cancel();
                refresh_listing();
             },
             error: function () {
                listing_cancel();
             }
        });
    } else {
        listing_cancel();
    }

}

function refresh_listing(done) {
    d3.json(url_for("listing.cgi"), function (data) {
        // console.log("data", data);
        var div = d3.select("#listing .body");
            item = div
                .selectAll("div.item")
                .data(data.items, function (d) { return d.path });

        var newitem = item.enter()
                .append("div")
                .attr("class", "item");
        newitem
            .append("input")
            .attr("class", "itemcheckbox")
            .attr("type", "checkbox")
            .on("change", checkbox_click);
        newitem
            .append("a")
            .text(function(d) { return d.path })
            .attr("href", function (d) { return d.url })
            .on("click", function (d) {
                var that = this;
                d3.event.preventDefault();
                if (d3.select(this).classed("rename")) return;
                if (longclick_begin) {
                    click_time = new Date().getTime() - longclick_begin;
                    if (click_time > 700 && click_time < 2500) {
                        item_longclick.call(this, d);
                        return;
                    }
                }
                if (d.remake) {
                    // alert("make");
                    make(d.path, function () {
                        // re-get the d in case of change!
                        var d = d3.select(that).datum();
                        // console.log("d", d, d.binary, d.url); 
                        if (!d.binary) {
                            edit(d.url);
                        } else {
                            preview(d.url);
                        }
                    });
                    return false;
                } else if (!d.binary) {
                    edit(d.url);
                } else {
                    preview(d.url);
                }               
            })
            .on("mousedown", function () {
                longclick_begin = new Date().getTime();
            });
        // console.log("item.update", item);
        item
            .select("a")
            .classed("normal", function (d) { return d.exists && !d.remake })
            .classed("make", function (d) { return d.exists && d.remake })
            .classed("potential", function (d) { return !d.exists })
            .classed("exists", function (d) { return d.exists })
            .classed("remake", function (d) { return d.remake });

        item.exit()
            .remove();

        item.order();

        if (done) {
            done.call(data, data);
        }
    });
}
refresh_listing();

$("#listing .body").niceScroll({cursorcolor:"#0F0"});
$("#editor .make .body").niceScroll({cursorcolor:"#0F0"});

$("#listing_refresh").click(refresh_listing);
$("#listing_delete").click(delete_selection);
$("#listing_rename").click(rename);
$("#listing_cancel").click(listing_cancel);
// $("#listing_select_all").click(select_all);

/* File drop */

$(function () {
    $('#listing').fileupload({
        url: url_for("upload.cgi"),
        dataType: 'json',
        done: function (e, data) {
            refresh_listing();
            console.log(data.result);
            //$.each(data.result.files, function (index, file) {
            //    $('<p/>').text(file.name).appendTo(document.body);
            //});
        }
    });
});
