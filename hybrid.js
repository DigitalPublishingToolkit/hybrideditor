function set_editor (text) {
    // var textarea = $("#editor textarea");
    // textarea.val(text);
    // var session = editor.createEditSession(text, "ace/mode/markdown");
    // editor.aceeditor.setSession(session);
    editor.setValue(text);
    editor.clearSelection();
    editor.scrollToRow(1);
}

function get_editor_text () {
  // return $("#editor textarea").val();
  return editor.getValue();
}

$("#previewform").on("submit", function () {
  //console.log("preview form submit")
  $("#previewformtext").val(get_editor_text());
  return true;
})

Dropzone.options.dropzone = {
  paramName: "file", // The name that will be used to transfer the file
  maxFilesize: 20, // MB
  // accept: function(file, done) {
  //   if (file.name == "justinbieber.jpg") {
  //     done("Naha, you don't.");
  //   }
  //   else { done(); }
  // },
  success: function (file, resp) {
    // console.log("success")
    $("#openmenu").hide();
    file.previewElement.classList.add("dz-success");
      //    file.previewElement.classList.remove("dz-error-mark");

    set_editor(resp);
    var pf = $("#previewform");
    // console.log("about to submit", pf.get(0));
    pf.submit();
  }   
};

$("#openbutton").click(function () {
  $("#openmenu").toggle();
});

aa_frames("#split");

var editor = ace.edit($("#editortext").get(0));
editor.setTheme("ace/theme/chrome");
editor.setHighlightActiveLine(false);
editor.setShowInvisibles(true);
editor.getSession().setMode("ace/mode/markdown");
editor.getSession().setUseWrapMode(true);

