ko.validation.registerExtenders();
/* setup ko validation */
ko.validation.init({
    decorateInputElement: true,
    errorElementClass: 'invalid',
    insertMessages: false

});
/*
TODO: combine all these models later on
*/
function Metadata(){
	var self = this;
	self.key = ko.observable().extend({
		required: true
	});
	self.value = ko.observable().extend({
		required: true
	});
}
function Tak () {
	var self = this;
	self.name = ko.observable().extend({
		required: true
	});
	self.lat = ko.observable().extend({
		required: true
	});
	self.lng = ko.observable().extend({
		required: true
	});
	self.metadata = ko.observableArray();
	self.creator = ko.observable();
	
	self.addMetadata = function(){
		var data = new Metadata();
		self.metadata.push(data);
		return data;
	};
	self.removeMetadata = function(data){
		/**
		*	also send delete to server
		*/
		 self.metadata.remove(data);
	};

}
function EditTakModel(){
	var self = this;
	self.tak =  ko.observable(new Tak());
	self.oldname;
	self.edit = ko.observable(false);
	self.createMetadata = ko.validatedObservable(new Metadata());

	self.pushMetadata = function(){
		/**
		* adds metadata by sending to server
		*/
		console.log("Button press");
		if(self.createMetadata.isValid()){
			var array = new Array();
			var obj = {
				"key": self.createMetadata().key(),
				"value": self.createMetadata().value()
			}
			array.push(obj);
			console.log(array);
			console.log(JSON.stringify(array));

			$.ajax({
		        type: "POST",
		        url: '/api/v1/tak/' + currentTakID + '/metadata/',
		        dataType: 'json',
		        contentType : 'application/json',
		        async: true,
		        data: JSON.stringify(array),
		        success: function (response) {
		        	 var obj = response; // reponse is an object so no need to parse reponse
                        console.log(obj)
		        	},
		        error: function(response){
		        	console.log(response.responseJSON);
                        alert("Error submitting: " + response.responseJSON.message);
		        }
		    });
			console.log("--valid");
			var data = self.tak().addMetadata();
			data.key(self.createMetadata().key());
			data.value(self.createMetadata().value());
			self.createMetadata().key(undefined);
			self.createMetadata().value(undefined);
			self.createMetadata().value.isModified(false);
			self.createMetadata().key.isModified(false);
		}

	}

	self.cancel = function(){
		self.tak().name(self.oldname);
		self.edit(!self.edit());
	}
	self.toggleEdit = function(){
		if(self.edit()){
			$.ajax({
		    url: '/api/tak/' + currentTakID,
		    data: { 'name': self.tak().name()},
		    type: 'PUT',
		    success: function(result) {
		        console.log(result);
		    }
			});
		}
		self.oldname = self.tak().name();
		self.edit(!self.edit());
	}
	$.getJSON("/api/tak/" + currentTakID, function(data) { 
	    var tak = new Tak();
	    tak.name(data.name);
	    tak.lat(data.lat);
	    tak.lng(data.lng);
	    tak.creator(data.creator.name);
	    for(var i = 0; i < data.metadata.length; i++){
	    	console.log(data.metadata[i]);
	    	var meta = tak.addMetadata();
	    	meta.key(data.metadata[i].key);
	    	meta.value(data.metadata[i].value);
	    }
		addMarker(data.lat, data.lng, {name: data.name});
	    self.tak(tak);
	});

	   
}
/**
*	bind data after page is loaded
*/
$(document).ready(function() {
	ko.applyBindings( new EditTakModel());

});
