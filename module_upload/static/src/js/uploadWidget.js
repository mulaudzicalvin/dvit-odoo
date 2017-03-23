openerp.module_upload = function(instance, local) {
	var _t = instance.web._t,
        _lt = instance.web._lt;
    var QWeb = instance.web.qweb;
    function performClick(elemId) {
	   var elem = document.getElementById(elemId);
	   if(elem && document.createEvent) {
	      var evt = document.createEvent("MouseEvents");
	      evt.initEvent("click", true, false);
	      elem.dispatchEvent(evt);
	   }
	}
    local.module_upload = instance.web.form.AbstractField.extend({
    	events: {
        	"click #BrowseButton": function(){
	        	$("#upload_module").click();
	        },
	        "change #upload_module": function() {
	        	self = this;
	        	var myFormData = new FormData($('#uploadModuleForm')[0]);
		        if (! self.get("effective_readonly")) {
		        	$.ajax({
			            type: 'POST',
			            url: '/upload_module',
			            cache: false,
				        contentType: false,
				        processData: false,
			            data: new FormData($('#uploadModuleForm')[0]),
			            success: function(result,status,xhr) {
					        self.internal_set_value(result);
			                self.$el.find("#pFileName").text(result.split('/').slice(-1)[0]);
				        }
			        });
		        }
	        },
	        "click #downloadButton": function() {
	        	var file = "/download/" + self.get("value").replace(/\//g,"'");
	        	self = this;
		        if ( self.get("effective_readonly")) {
		        	$.ajax({
			            type: 'POST',
			            url: file,
			            success: function(result,status,xhr) {
			            	window.location = file;
				        }
			        });
		        }
		    }
    	},
	    init: function() {
	    	var self = this;
	        self._super.apply(self, arguments);
	        self.set("value", "");
	    },
	    start: function() {
	    	self = this;
	        self.on("change:effective_readonly", self, function() {
				if ( self.get("effective_readonly")) {
				}
	            self.display_field();
	            self.render_value();
	        });
	        self.display_field();
	        self.render_value();

	        return this._super();
	    },
	    display_field: function() {
	        self = this;
	        self.$el.html(QWeb.render("MAKUpload", {widget: self}));
	    },
	    render_value: function() {
	    	self = this;
	        try {
			    if (self.get("effective_readonly")) {
		            self.$el.find("#pFileName").text(self.get("value").split('/').slice(-1)[0]);
		        } else {
		            self.$el.find("#pFileName").text(self.get("value").split('/').slice(-1)[0]);
		        }
			}
			catch(err) {
				console.log(err);
			}
	    },
	    get_this_value: function(){
	    	self = this;
	    	try {
			    self.get("value").split("/").slice(-1)[0];
			    return self.get("value").split("/").slice(-1)[0];
			}
			catch(err) {
				console.log(err);
			}
	    	
	    },
	});

	instance.web.form.widgets.add('module_upload', 'instance.module_upload.module_upload');
}