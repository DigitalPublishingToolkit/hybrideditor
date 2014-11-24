// aa.frames = aa_frames;

/* ******************* */
/* Simple css "frames" */
/* ******************* */

// todo: add an explicit flip button/area
function aa_frames (elt) {

    var units = "px"; // or %
    $(elt).find(".hdiv").draggable({
        axis: 'x',
        drag: function (evt, ui) {
            var c = $(evt.target.parentNode),
                cw = c.width(),
                l, r;
            if (units == "px") {
                l = ui.position.left;
                r = cw-l;
            } else {
                l = (ui.position.left/cw)*100;
                r = 100-l;
            }
            c.find(".left").css("right", r+units);
            c.find(".right").css("left", l+units);
            c.find(".left,.right").trigger("resize");
        },
        stop: function (evt) {
            var c = $(evt.target.parentNode);
            c.find(".left,.right").trigger("resize");
        },
        iframeFix: true
    }).click(function (evt) {
        // console.log("FLIP", evt, this);
        var c = $(this.parentNode);
                cw = c.width(),
                l, r,
                left = c.find(".left"),
                right = c.find(".right");

        if (units == "px") {
            l = $(this).position().left;
            r = cw-l;
        } else {
            l = ($(this).position().left/cw)*100;
            r = 100-l;
        }
        
        // switch lefts to rights
        left.removeClass("left").addClass("right").css("right", '');
        right.removeClass("right").addClass("left").css("left", '');

        // do a drag...
        c.find(".left").css("right", r+units);
        c.find(".right").css("left", l+units);
        c.find(".left,.right").trigger("resize");

    }).append('<div class="divcontents"></div>');

    $(elt).find(".vdiv").draggable({
        axis: 'y',
        drag: function (evt, ui) {
            var c = $(evt.target.parentNode),
                ch = c.height(),
                t = ui.position.top,
                b = ch-t;
            c.find(".top").css("bottom", b+"px");
            c.find(".bottom").css("top", t+"px");
            c.find(".top,.bottom").trigger("resize");
        },
        stop: function (evt) {
            var c = $(evt.target.parentNode);
            c.find(".top,.bottom").trigger("resize");
        },
        iframeFix: true
    }).click(function (evt) {
        // console.log("FLIP", this);
        var c = $(this.parentNode),
            ch = c.height(),
            t = $(this).position().top,
            b = ch-t,
            top = c.find(".top"),
            bottom = c.find(".bottom");
        // console.log(c, ch, t, b, top, bottom);
        // switch lefts to rights
        top.removeClass("top").addClass("bottom").css("bottom", '');
        bottom.removeClass("bottom").addClass("top").css("top", '');

        // do a drag...
        c.find(".top").css("bottom", b+"px");
        c.find(".bottom").css("top", t+"px");
        c.find(".top,.bottom").trigger("resize");

    }).append('<div class="divcontents"></div>');

};
