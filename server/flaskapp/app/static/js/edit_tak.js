
function Tak () {
	var self = this;
	self.name = ko.observable();
	self.lat = ko.observable();
	self.lng = ko.observable();
	self.creator = ko.observable();
}
function EditTakModel(){
	var self = this;
	self.tak =  ko.observable(new Tak());
	self.oldname;
	self.edit = ko.observable(false);
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
