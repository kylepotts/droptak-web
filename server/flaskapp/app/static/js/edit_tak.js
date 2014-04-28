ko.validation.registerExtenders();
/* setup ko validation */
ko.validation.init({
    decorateInputElement: true,
    errorElementClass: 'invalid',
    insertMessages: false

});
var tmarker;
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
	self.loading = ko.observable(false);
}
function Map(){
	var self = this;
	self.name = ko.observable();
	self.id = ko.observable();
	self.moveTo = function(cmapid){
		if(self.id() == cmapid) return;
		console.log("move to " + self.name());
		$.ajax({
		    url: '/api/v1/tak/' + currentTakID + '/?mapid=' + self.id(),
		    type: 'PUT',
		    success: function(response) {
		        window.location.reload();
		    },
		    error: function(response){
		    	alert("Error submitting: " + response.responseJSON.message);
		    },
		    complete: function(response){
		    	console.log(response.responseJSON);
		    }
		});
	}
	self.copyTo = function(cmapid){
		if(self.id() == cmapid) return;
		console.log("copy to " + self.name());
		$.ajax({
		    url: '/api/v1/tak/' + currentTakID + '/copy/?mapid=' + self.id(),
		    type: 'POST',
		    success: function(response) {
		       	alert("Copied successfully");
		    },
		    error: function(response){
		    	alert("Error submitting: " + response.responseJSON.message);
		    },
		    complete: function(response){
		    	console.log(response.responseJSON);
		    }
		});
	}
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
	self.map = ko.observable(new Map());
	self.metadata = ko.observableArray();
	self.creator = ko.observable();
	
	self.addMetadata = function(){
		var data = new Metadata();
		self.metadata.push(data);
		return data;
	};
	self.removeMetadata = function(data){
		var key = encodeURIComponent(data.key());
		data.loading(true);
		$.ajax({
		    url: '/api/v1/tak/' + currentTakID + '/metadata/' + key + '/',
		    type: 'DELETE',
		    success: function(response) {
		        self.metadata.remove(data);
		    },
		    error: function(response){
		    	alert("Error submitting: " + response.responseJSON.message);
		    },
		    complete: function(response){
		    	console.log(response.responseJSON);
		    	data.loading(false);
		    }
		});
	}

}
var editMode = false;
var cTak;
function EditTakModel(){
	var self = this;
	self.tak =  ko.validatedObservable(new Tak());
	cTak = self.tak;
	self.oldTak = new Tak();
	self.selectedMap = ko.observable();
	self.edit = ko.observable(false);
	editMode = self.edit;
	self.maps = ko.observableArray();
	self.createMetadata = ko.validatedObservable(new Metadata());
	self.addMap = function () {
		var map = new Map();
		self.maps.push(map);
		return map;
	};
	$.getJSON("/maps", function (data) {
		console.log(data);
		for (var i = 0; i < data.length; i++) {
			var local = self.addMap();
			local.name(data[i].name);
			local.id(data[i].id)
		}
	});
	self.pushMetadata = function(){
		/**
		* adds metadata by sending to server
		*/
		console.log("Button press");
		if(self.createMetadata.isValid()){
			self.createMetadata().loading(true);
			var array = new Array();
			var obj = {
				"key": self.createMetadata().key(),
				"value": self.createMetadata().value()
			}
			array.push(obj);
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

					var data = self.tak().addMetadata();
					data.key(self.createMetadata().key());
					data.value(self.createMetadata().value());
					self.createMetadata().key(undefined);
					self.createMetadata().value(undefined);
					self.createMetadata().value.isModified(false);
					self.createMetadata().key.isModified(false);
		        	},
		        error: function(response){
		        	console.log(response.responseJSON);
                    alert("Error submitting: " + response.responseJSON.message);
		        },
		        complete: function(response){
		        	self.createMetadata().loading(false);
		        }
		    });
			
		}

	}

	self.cancel = function(){
		self.tak().name(self.oldTak.name());
		self.tak().lat(self.oldTak.lat());
		self.tak().lng(self.oldTak.lng());
		self.edit(!self.edit());
		if(tmarker !== undefined ) tmarker.setMap(null);
	}
	self.toggleEdit = function(){
		if(self.edit()){
			if(self.tak().name.isValid() && self.tak().lng.isValid() && self.tak().lat.isValid()){
				console.log("Valid")
				var query = '?name=' + encodeURIComponent(self.tak().name())
				query += '&lat=' + encodeURIComponent(self.tak().lat())
				query += '&lng=' + encodeURIComponent(self.tak().lng())
				$.ajax({
			    url: '/api/v1/tak/' + currentTakID + '/' + query,
			    type: 'PUT',
			    success: function(result) {
			        console.log(result);
			        window.location.reload();
			        self.edit(!self.edit());
			    },
			    error: function(result){
			    	console.log(result);
			    	alert("Error submitting.");
			    }
				});
			}
			else{
				alert("Invalid Data");
			}
		}
		else{
			self.oldTak.name(self.tak().name());
			self.oldTak.lng(self.tak().lng());
			self.oldTak.lat(self.tak().lat());
			if(tmarker !== undefined ) tmarker.setMap(null);
			self.edit(!self.edit());
		}
		
		
	}
	$.getJSON("/api/tak/" + currentTakID, function(data) { 
	    var tak = new Tak();
	    tak.name(data.name);
	    tak.lat(data.lat);
	    tak.lng(data.lng);
	    tak.creator(data.creator.name);
	    tak.map().id(data.map.id);
	    tak.map().name(data.map.name);
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
