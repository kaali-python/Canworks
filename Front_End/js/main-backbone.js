
$(document).ready(function(){
   	App = {} ;
	window.App = App ;


function make_request(data){
	url =  "http://localhost:8000/process_text" ;
	return 	$.post(url, {"text": data})
		}

/*This is the template object which uses name as an argument to return handlebar compiled template from the the html
 */
var template = function(name){
    return Mustache.compile($("#"+name+"-template").html());
};



App.RootView = Backbone.View.extend({
	tagName: "form",
	className: "form-horizontal",
	template: template("root"),
	initialize: function(){
		console.log("Root view called")
	},
	render: function(){
		this.$el.append(this.template(this));
		return this;
	},
	events: {
		"click #submitQuery": "submitQuery",
	},

	submitQuery: function(event){
		event.preventDefault();
		$(".dynamic_display").empty()
		var jqhr = make_request($("#searchQuery").val())
		jqhr.done(function(data){
			if (data.error == false){
				data.overall_sentiment
				var subView = new App.RootTopView({model: {"sentiment": data.overall_sentiment, "phrases": data.noun_phrase}})
				$(".dynamic_display").append(subView.render().el);	
				$.each(data.result, function(iter, text){
					var subView = new App.RootRowView({model: text});
					$(".dynamic_display").append(subView.render().el);	
				})
						}
			else{
				bootbox.alert(data.messege)	
			}
			})
	},
});

App.RootTopView = Backbone.View.extend({
	tagName: "fieldset",
	className: "well plan",
	template: template("root-top"),

	phrases: function(){return this.model.phrases},
	sentiment: function(){return this.model.sentiment},
	
	initialize: function(options){
		this.model = options.model;
	},
	render: function(){
		this.$el.append(this.template(this));
		return this;
	},

});


App.RootRowView = Backbone.View.extend({
	tagName: "fieldset",
	className: "well plan",
	template: template("root-row"),

	noun_phrases: function(){return this.model.noun_phrases},
	polarity: function(){return this.model.polarity},
	sentence: function(){return this.model.sentence},
	tag: function(){return this.model.tag},
	initialize: function(options){
		this.values = {"food": 1, "service": 2, "ambience": 3, "cost": 4, "null": 5};
		this.model = options.model;
	},
	render: function(){
		this.$el.append(this.template(this));
		this.$("#ddpFilter option[value='" + this.values[this.model.tag] + "']").attr("selected", "selected")
		return this;
	},

	events: {
		    "change #ddpFilter" : "changeTag"
	},

	changeTag: function(event){
		var self = this;
		event.preventDefault()
		bootbox.confirm("Are you sure you want to change the tag of this sentence?", function(result) {
			if (result == true){
				changed_tag = self.$('#ddpFilter option:selected').text();
				sentence = self.sentence();

				var jqhr = $.post("http://localhost:8000/update_model", {"text": sentence, "tag": changed_tag})	
				jqhr.done(function(data){
					if (data.messege == "success"){
						bootbox.alert("Tag has been changed")
						}
					else {
						bootbox.alert(data.messege)
					}	
				})
				
				jqhr.fail(function(){
					bootbox.alert("Either the api or internet connection is not working, Try again later")
				})
			
				}	
		}); 
	},
});



App.Router = Backbone.Router.extend({
	initialize: function(options){
		this.el =  options.el ;
	},

	routes: {
		"":  "welcome",
	},
	
	welcome: function(){
		var str = new App.RootView()
		this.el.html(str.render().el);
	},
});

App.boot = function(container){
	container = $(container);
	var router = new App.Router({el: container});
	Backbone.history.start();
}
});



