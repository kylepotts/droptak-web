ko.validation.registerExtenders();
/* setup ko validation */
ko.validation.init({
	decorateInputElement: true,
	errorElementClass: 'invalid',
	insertMessages: true

});
function Tak() {
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
	self.map = ko.observable().extend({
		required: true
	});
}
var cTak = ko.validatedObservable(new Tak());
function Map(){
	var self = this;
	self.name = ko.observable();
	self.id = ko.observable();
}
function CreateTakModel(){
	var self = this;
	self.currenttak = cTak;
	self.maps = ko.observableArray();
	self.newMapName = ko.observable().extend({
		required: true
	});
	self.createdTaks = ko.observableArray();
	self.isPublic = ko.observable('0');
	self.createMap = function(isPublic, callback){
		console.log("Creating Map");

		$.post('/maps/new', {
			name: self.newMapName(),
			isPublic: isPublic
		})
		.done(function (response) {
			var obj = response; // reponse is an object so no need to parse reponse
			console.log(obj)
			//and display it locally
			var map = self.addMap();
			map.name(obj.name);
			map.id(obj.id);
			self.newMapName("");
			self.maps().push(map);
			cTak().map(map);
			callback();
		})
		.fail(function (response) {
			console.log(response.responseJSON);
			alert("Error submitting: " + response.responseJSON.message);
		});
	}
	self.createTak = function(){
		if(cTak().isValid()){
			console.log("Creating tak");
			console.log(self.currenttak().name());
			console.log(self.currenttak().lat());
			console.log(self.currenttak().lng());
			console.log(self.currenttak().map().id());

			var mapId = self.currenttak().map().id();
			var title = self.currenttak().name();
			var lat = self.currenttak().lat();
			var lng = self.currenttak().lng();
			$.post('/create/', {
					title: title,
					mapId: mapId,
					lat: lat,
					lng: lng
				})
				.done(function (response) {
					var obj = response; // reponse is an object so no need to parse reponse
						console.log(obj)
						var tak = new Tak();
						tak.name(obj.name);
						tak.lat(obj.lat);
						tak.lng(obj.lng);
						self.createdTaks.push(tak);
						setMarkers(ko.toJS(self.createdTaks));
						cTak().name(undefined);
						cTak().lat(undefined);
						cTak().lng(undefined);
						self.newMapName(undefined);
						cTak().name.isModified(false);
						cTak().lat.isModified(false);
						cTak().lng.isModified(false);
						self.newMapName.isModified(false);
						cTak().map(self.newMap);
				})
				.fail(function (response) {
					console.log(response.responseJSON);
					alert("Error submitting: " + response.responseJSON.message);
				});
		}
	}
	self.submit = function(){
		if(cTak().isValid()){
			if(cTak().map().id() < 0 ){
				// create map
				if(self.newMapName.isValid()){
					console.log(self.newMapName());
					var isPublic = false;
					if(self.isPublic() == '1'){
						isPublic = true;
					}
					console.log(isPublic);
					self.createMap(isPublic, self.createTak);
					return;
					
				}
				else{
					// invlaid map anem
					alert("Invalid input");
					return;
				}
			}
			else{
				self.createTak();
				return;
			}
			
		}
		alert("Invalid input");
		return;
		
	};
	self.addMap = function () {
		var map = new Map();
		self.maps.push(map);
		return map;
	};
	self.newMap = self.addMap();
	self.newMap.name("New Map");
	self.newMap.id(-1);
	$.getJSON("/maps", function (data) {
		console.log(data);
		for (var i = 0; i < data.length; i++) {
			var local = self.addMap();
			local.name(data[i].name);
			local.id(data[i].id)
		}
	});


}
$(document).ready(function () {
	ko.applyBindings(new CreateTakModel());
});