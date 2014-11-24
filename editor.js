var editor_factory = aa_aceeditor(window.ace),
    editor = editor_factory.get_editor(),
    listing_url = d3.select("link[rel='listing-data-source']").attr("href"),
    save_url = d3.select("link[rel='save-url']").attr("href")
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
    make_busy = make_div
        .append("div")
        .attr("class", "busy");

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
        url: save_url,
        method: "post",
        data: {
            text: data.text,
            f: path_for_href(data.href)
        },
        dataType: "json",
        success: function (data) {
            console.log("save.success", data);
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
make_busy.append("img")
    .attr("src", "/imgs/gear.gif");

aa_frames(document.getElementById("split"));

document.getElementById("editor").appendChild(editor.elt);

function edit (url) {
    editor.href(url);
    preview_div
        .style("display", "none");
    make_div.style("display", "none");
}

function preview (url) {
    preview_div
        .style("display", "block");
    preview_iframe
        .attr("src", url);
    make_div.style("display", "none");
}

function make (path, done) {
    // console.log("make", path);
    var make_url = d3.select("link[rel='make-url']").attr("href");
    make_div.style("display", "block");
    make_busy.style("display", "block");
    make_url += "&f="+encodeURIComponent(path);
    d3.json(make_url, function (data) {
         d3.select("#editor .make .stdout").text(data.stdout);
         d3.select("#editor .make .stderr").text(data.stderr);
         make_busy.style("display", "none");
         refresh_listing();
         if (done) {
            done.call(data, data);
         }
    });
}

function update_selection() {
    var checkboxes = d3.selectAll(".itemcheckbox"),
        checked = d3.selectAll(".itemcheckbox:checked"),
        ss = checked.size(),
        select_all_button = d3.select("#listing_select_all"),
        selfunk = d3.select("#listing .selection_functions");
    if (ss >= 1) {
        selfunk.style("display", "inline");
    } else {
        selfunk.style("display", "none");
    }
    if (ss > 0 && ss == checkboxes.size()) {
        select_all_button.text("deselect all");
    } else {
        select_all_button.text("select all");
    }
}

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

function delete_selection () {
    var rm_url = d3.select("link[rel='rm-url']").attr("href"),
        checked = d3.selectAll(".itemcheckbox:checked"),
        ss = checked.size(),
        paths = checked.data().map(function (d) { return d.path });

    if (ss == 0) return;
    var ok = confirm("Delete " + ss + " items?");
    if (ok) {
        $.ajax({
             url: rm_url,
             method: "post",
             data: {
                 'f[]': paths 
             },
             dataType: "json",
             success: function (data) {
                checked.property("checked", false);
                update_selection();
                // console.log("rm response", data);
                refresh_listing();
             }
        });
    }
}

function refresh_listing() {
    d3.json(listing_url, function (data) {
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
            .on("change", update_selection);
        newitem
            .append("a")
            .text(function(d) { return d.path })
            .attr("href", function (d) { return d.url })
            .on("click", function (d) {
                d3.event.preventDefault();
                // console.log("d", d);
                if (d.remake) {
                    // alert("make");
                    make(d.path, function () {
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

    });
}
refresh_listing();

$("#listing .body").niceScroll({cursorcolor:"#0F0"});
$("#listing_refresh_button").click(refresh_listing);
$("#listing_delete_selection").click(delete_selection);
$("#listing_select_all").click(select_all);
