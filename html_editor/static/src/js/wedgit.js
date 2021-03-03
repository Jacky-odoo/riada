odoo.define('html_editor.sm_editor', function (require) {
"use strict";

var basic_fields = require('web.basic_fields');
var core = require('web.core');
var InField = require('web.basic_fields').InputField;
var _t = core._t;
var _lt = core._lt;
var ajax = require('web.ajax');


//var Text = basic_fields.FieldText;
//Text.include({
var Text = InField.extend({
    description: _lt("Text"),
    jsLibs: [
        '/html_editor/static/src/ckeditor/ckeditor.js',
    ],
//    cssLibs: [
//        '/html_editor/static/src/summernote/summernote.min.css',
//    ],
    /**
     *
     * @override
     * @private
     */
    _render: function () {
        var def = this._super.apply(this, arguments);
        //this.nodeOptions.enable_code
        if (this.mode == "edit") {
            var input = this.$el[0];
            $(document).ready(function(){
                if(input){
                    var editorId = $(input).attr('id');
                    var editorContent = $(input).val()
                    var editorElement = CKEDITOR.document.getById( editorId );
                    var editor = CKEDITOR.replace(editorId);
                    editor.setData(editorContent);

                    editor.on('key', function(e) {
                        var content = editor.getData();
                        $(input).val(content).trigger('change');
                    });



                    editor.on('change', function(e) {
                        var content = editor.getData();
                        $(input).val(content).trigger('change');
                        console.log($(input).val())
                        alert("changed...")
                    });

                }
            });
            return def;
        }else{
            var input = this.$el[0];
            var html = $(input).html();
            var doc = new DOMParser().parseFromString(html, "text/html");
            $(input).empty().append(doc.documentElement.textContent)
        }
    },
});

return {
    Text:Text,
}

//return Text;

});
odoo.define('html_editor._sm_editor_widget', function (require) {
    "use strict";
    var registry = require('web.field_registry');
    var sm_editor = require('html_editor.sm_editor')
    registry.add('sm_editor', sm_editor.Text);
});
