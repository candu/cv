dojo.require("dijit.Editor");

dojo.require("dijit._editor.plugins.FullScreen");
dojo.require("dijit._editor.plugins.ViewSource");
dojo.require("dojox.editor.plugins.AutoUrlLink");
dojo.require("dojox.editor.plugins.Blockquote");
dojo.require("dojox.editor.plugins.CollapsibleToolbar");
dojo.require("dojox.editor.plugins.FindReplace");
dojo.require("dojox.editor.plugins.NormalizeIndentOutdent");
dojo.require("dojox.editor.plugins.PrettyPrint");

dojo.ready(function(){
  var textareas = dojo.query("textarea");
  if(textareas && textareas.length){
    dojo.addClass(dojo.body(), "claro");
    textareas.instantiate(dijit.Editor, {
      styleSheets: "/static/css/base.css",
      plugins: [
        "collapsibletoolbar",
        "fullscreen", "viewsource", "|",
        "undo", "redo", "|",
        "bold", "italic", "underline", "strikethrough", "|",
        "insertOrderedList", "insertUnorderedList", "indent", "outdent", "||",
      ]
    });
  }
});
