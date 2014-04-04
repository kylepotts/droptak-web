
function Tak () {
	var self = this;
	self.title = ko.observable();
	self.lat = ko.observable();
	self.lng = ko.observable();
	self.creator = ko.observable();
}
function EditTakModel(){
	var self = this;
	self.tak =  ko.observable(new Tak());
	self.oldTitle;
	self.edit = ko.observable(false);
	self.cancel = function(){
		self.tak().title(self.oldTitle);
		self.edit(!self.edit());
	}
	self.toggleEdit = function(){
		if(self.edit()){
			$.ajax({
		    url: '/api/tak/' + currentTakID,
		    data: { title: self.tak().title()},
		    type: 'PUT',
		    success: function(result) {
		        console.log(result);
		    }
			});
		}
		self.oldTitle = self.tak().title();
		self.edit(!self.edit());
	}
	$.getJSON("/api/tak/" + currentTakID, function(data) { 
	    var tak = new Tak();
	    tak.title(data.title);
	    tak.lat(data.lat);
	    tak.lng(data.lng);
	    tak.creator(data.creator);
		addMarker(data.lat, data.lng, {title: data.title});
	    self.tak(tak);
	});

	   
}
/**
*	bind data after page is loaded
*/
$(document).ready(function() {
	ko.applyBindings( new EditTakModel());

});
