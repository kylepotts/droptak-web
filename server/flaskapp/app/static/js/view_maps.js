ko.validation.rules['unique'] = {
    validator: function (val, otherVal) {
    	/*eventually use to check if item exists
			unique: true,
    	*/
        return val === otherVal;
    },
    message: 'The field must equal {0}'
};
ko.validation.registerExtenders();
/* setup ko validation */
ko.validation.init( {
	decorateInputElement: true,
	errorElementClass: 'invalid',
	insertMessages: true

});

/**
* generate uids for data-binding in dom
*/
ko.bindingHandlers.uniqueId = {
    init: function(element, valueAccessor) {
        var value = valueAccessor();
        value.id = value.id || ko.bindingHandlers.uniqueId.prefix + (++ko.bindingHandlers.uniqueId.counter);

        element.id = value.id;
    },
    counter: 0,
    prefix: "unique"
};

ko.bindingHandlers.uniqueFor = {
    init: function(element, valueAccessor) {
        var value = valueAccessor();
        value.id = value.id || ko.bindingHandlers.uniqueId.prefix + (++ko.bindingHandlers.uniqueId.counter);

        element.setAttribute("for", value.id);
    } 
};
/**
*	Knockout models for data binding
*/

function Tak(){
	var self 				= this;
	self.title      = ko.observable();
	self.lat        = ko.observable();
	self.lng  			= ko.observable();

}
function FormMap(){
	var self = this;
	self.name = ko.observable().extend({
		required: true,
		minLength: 1
	});
}
function Map(){
	var self        = this;
	self.name      = ko.observable();
	self.id 				= ko.observable();
	self.taks  			= ko.observableArray();

	self.addTak = function(){
			self.taks.push( new Tak());
		}
	self.addTak();
	self.removeTak = function(tak){
			self.taks.remove(tak);
		}



}
/**
*	Highest level model for entire app
*/
function MapTakModel() {
	var self      	= this;
	self.maps 	  	= ko.observableArray();
	self.selected		= ko.observable();
	self.form 			= new FormMap();

	/**
	* add a new map
	*/
	self.addMap= function() { 
			var map = new Map();
			self.maps.push(map);
			return map;
		};

	self.submit = function(modal){
			// check if form is valid
			console.log("submit");
			console.log(self.form.name());
			if(self.form.name.isValid()){
				console.log("valid");
				// if it is, then submit it to server
				$.post('/maps/new',{name: self.form.name()}) 
					.done(function() {
				    	//alert( "Submitted" );
				    	//and display it locally
				    	self.addMap().name(self.form.name());
				    	self.form.name(undefined);
							self.form.name.isModified(false);
							$(modal).modal("hide");
					})
					.fail(function() {
						alert( "Error submitting" );
					});
			}
		};

	/**
	* remove a map from model
	*/
	self.removeMap = function(map) {
			self.maps.remove(map);
		};

	$.getJSON("/maps", function(data) { 
	    // Now use this data to update your view models, 
	    // and Knockout will update your UI automatically 
	    for (var i = 0; i < data.length; i++) { 
	    	var local = self.addMap();
	    	local.name(data[i].name);
			}
		});
}

/**
*	bind data after page is loaded
*/
$(document).ready(function() {
	ko.applyBindings( new MapTakModel());
});

