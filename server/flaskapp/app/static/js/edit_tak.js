function Tak () {
	var self = this;
	self.title = ko.observable();
	self.lat = ko.observable();
	self.lng = ko.observable();
}
function EditTakModel(){
	var self = this;
	self.tak = ko.observable();
	self.edit = ko.observable(false);

	self.toggleEdit = function(){
		self.edit(!self.edit());
	}
}
/**
*	bind data after page is loaded
*/
$(document).ready(function() {
	ko.applyBindings( new EditTakModel());
});
