$(document).ready(function(){
    console.log("ready");
    $('.btn-toggle').click(function() {
    $(this).find('.btn').toggleClass('active');  
    
    if ($(this).find('.btn-primary').size()>0) {
        console.log("toggle to private")
        $(this).find('.btn').toggleClass('btn-primary');
    }    
    $(this).find('.btn').toggleClass('btn-default');
    var val = $('#toggleGroup .active').data("value")
       
});

});

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
ko.validation.init({
    decorateInputElement: true,
    errorElementClass: 'invalid',
    insertMessages: true

});

/**
 * generate uids for data-binding in dom
 */
ko.bindingHandlers.uniqueId = {
    init: function (element, valueAccessor) {
        var value = valueAccessor();
        value.cuid = value.cuid || ko.bindingHandlers.uniqueId.prefix + (++ko.bindingHandlers.uniqueId.counter);

        element.id = value.cuid;
    },
    counter: 0,
    prefix: "unique"
};

ko.bindingHandlers.uniqueFor = {
    init: function (element, valueAccessor) {
        var value = valueAccessor();
        value.cuid = value.cuid || ko.bindingHandlers.uniqueId.prefix + (++ko.bindingHandlers.uniqueId.counter);

        element.setAttribute("for", value.cuid);
    }
};
ko.bindingHandlers.urlFor = {
    update: function (element, valueAccessor) {
        var value = valueAccessor();
        element.setAttribute("href", "/maps/" + value.id());
    }
};

/**
 *	Knockout models for data binding
 */

function Tak() {
    var self = this;
    self.name = ko.observable();
    self.lat = ko.observable();
    self.lng = ko.observable();

}
function MapNameForm() {
    var self = this;
    self.currentMap = ko.observable();
    self.name = ko.observable().extend({
        required: true,
        minLength: 1
    });
}

function FormMap() {
    var self = this;
    self.name = ko.observable().extend({
        required: true,
        minLength: 1
    });
}

function addAdminForm() {
    var self = this;
    self.email = ko.observable().extend({
        required: true,
        minLength: 1
    });
}

function Map() {
    var self = this;
    self.name = ko.observable();
    self.id = ko.observable();
    self.isPublic = ko.observable();
    self.taks = ko.observableArray();

    self.addTak = function () {
        var tak = new Tak();
        self.taks.push(tak);
        return tak;
    }
    self.removeTak = function (tak) {
        self.taks.remove(tak);
    }

}
/**
 *	Highest level model for entire app
 */
function MapTakModel() {
    var self = this;
    self.maps = ko.observableArray();
    self.favorites = ko.observableArray();
    self.selected = ko.observable();
    self.loading = ko.observable(true);
    self.loadingFavorites = ko.observable(true);
    self.selectedIsAdmin = ko.observable(false);
    self.mapNameForm = new MapNameForm();
    self.mapNameFormLoading = ko.observable(false);

    self.form = new FormMap();
    self.modalSubmit = ko.observable(false);
    self.adminForm = new addAdminForm();


    self.mapNameFormSubmit = function(modal){
        
        if(self.mapNameForm.name() == self.mapNameForm.currentMap().name()) return ;
        console.log(self.mapNameForm.name());
        if(!self.mapNameFormLoading()){
            if(self.mapNameForm.name.isValid()){
                self.mapNameFormLoading(true);
                var query = '?name=' + encodeURIComponent(self.mapNameForm.name())
                $.ajax({
                url: '/api/v1/map/' + self.mapNameForm.currentMap().id() + '/' + query,
                type: 'PUT',
                success: function(result) {
                    console.log(result);
                    self.mapNameForm.currentMap().name(self.mapNameForm.name());
                    $(modal).modal("hide");

                },
                error: function(result){
                    console.log(result);
                    alert("Error submitting.");
                },
                complete: function(result){
                    self.mapNameFormLoading(false);
                }
                });


                

            }
            else console.log("Invalid");
        }
        else console.log("loading");
    }

    self.select = function (element, mapid, isAdmin) {
        self.selected(element);
        self.selectedIsAdmin(isAdmin);
        self.mapNameForm.currentMap(element);
        self.mapNameForm.name(element.name());
        console.log(element.id());
        setCookie("mapId", element.id(), 10)
        console.log(element.taks());
        setMarkers(ko.toJS(element.taks));
    }

    /**
     * add a new map
     */
    self.addMap = function () {
        var map = new Map();
        self.maps.push(map);
        return map;
    };

    self.submit = function (modal) {
        // check if form is valid
        if (!self.modalSubmit()) {
            self.modalSubmit(true);
            console.log("submit");
            var val = $('#toggleGroup .active').data("value")
            var isPublic;
            if(val == 1){
                isPublic = true;
            }

            if(val == 0){
                isPublic = false;
            }
            console.log("isPublic="+isPublic);
            console.log(self.form.name());
            if (self.form.name.isValid()) {
                console.log("valid");
                // if it is, then submit it to server
                $.post('/maps/new', {
                    name: self.form.name(),
                    isPublic: isPublic
                })
                    .done(function (response) {
                        var obj = response; // reponse is an object so no need to parse reponse
                        console.log(obj)
                        //and display it locally
                        var map = self.addMap();
                        map.name(obj.name);
                        map.id(obj.id);
                        map.isPublic(obj.public);
                        // reset form and hide it
                        self.form.name(undefined);
                        self.form.name.isModified(false);
                        self.modalSubmit(false);
                        $(modal).modal("hide");

                    })
                    .fail(function (response) {
                        console.log(response.responseJSON);
                        self.modalSubmit(false);
                        alert("Error submitting: " + response.responseJSON.message);
                    });
            } else {
                //invalid form
                self.modalSubmit(false);
            }
        }
    }


    self.addAdmin = function (data, modal) {
        // check if form is valid
        console.log("addAdmin mapId=" + self.selected().id())
        if (self.adminForm.email.isValid()) {
            self.loading(true);
            console.log("valid");
            // if it is, then submit it to server
            $.post('/map/admin/' + self.selected().id() + '/' + self.adminForm.email(), {})
                .done(function (response) {
                    console.log(response);
                     self.loading(false);
                    var obj = jQuery.parseJSON(response)
                    if(obj.hasOwnProperty("error")){
                        alert(obj['error']);
                        return;
                    }
                    // parse JSON text response
                    var obj = jQuery.parseJSON(response);;
                    //and display it locally
                    //var map = self.addMap();
                    //map.name(obj.name);
                    //map.id(obj.id);
                    // reset form and hide it
                    self.form.name(undefined);
                    self.form.name.isModified(false);
                    $(modal).modal("hide");
                })
                .fail(function () {
                    alert("Error submitting");
                     self.loading(false);
                });

        }

    };
    /**
     * remove a map from model
     */
    self.removeMap = function (map) {
        //send delete to server
        if (!confirm("Are you sure you want to permanently delete this map?")) return;
        self.loading(true);
        $.ajax({
            url: '/api/maps/' + map.id(),
            type: 'DELETE',
            success: function (result) {
                self.maps.remove(map);
                self.selected(null);
                console.log(result);
            },
            complete: function(result){
                self.loading(false);
            }
        });
    };
    self.unFavoriteMap = function (map) {
        //send delete to server
        if (!confirm("Are you sure you want to unfavorite this map?")) return;
        self.loading(true);
        $.ajax({
            url: '/api/v1/user/' + currentUserID + '/favorites/?mapid=' + map.id(),
            type: 'DELETE',
            success: function (result) {
                self.favorites.remove(map);
                self.selected(null);
                console.log(result);
            },
            complete: function(result){
                self.loading(false);
            }
        });
    };

    $.getJSON("/maps", function (data) {
        // Now use this data to update your view models, 
        // and Knockout will update your UI automatically 
        console.log(data);
        for (var i = 0; i < data.length; i++) {
            var local = self.addMap();
            local.name(data[i].name);
            local.id(data[i].id)
            local.isPublic(data[i].public);
            var taks = data[i].taks;
            for (var j = 0; j < taks.length; j++) {
                    var tak = local.addTak();
                    tak.name(taks[j].name);
                    tak.lat(taks[j].lat);
                    tak.lng(taks[j].lng);
                }
        }
        self.loading(false);
    });
    $.getJSON("/favorites", function (data) {
        // Now use this data to update your view models, 
        // and Knockout will update your UI automatically 
        console.log(data);
        for (var i = 0; i < data.length; i++) {
            var local = new Map();
            self.favorites.push(local);
            local.name(data[i].name);
            local.id(data[i].id)
            local.isPublic(data[i].public);
            var taks = data[i].taks;
            for (var j = 0; j < taks.length; j++) {
                    var tak = local.addTak();
                    tak.name(taks[j].name);
                    tak.lat(taks[j].lat);
                    tak.lng(taks[j].lng);
                }
        }
        self.loadingFavorites(false);
    });
}
/**
 *	bind data after page is loaded
 */
$(document).ready(function () {
    ko.applyBindings(new MapTakModel());
});

function setCookie(cname, cvalue, exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
    var expires = "expires=" + d.toGMTString();
    document.cookie = cname + "=" + cvalue + "; " + expires;
}

function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i].trim();
        if (c.indexOf(name) == 0) return c.substring(name.length, c.length);
    }
    return "";
}

function checkCookie() {
    var user = getCookie("username");
    if (user != "") {
        alert("Welcome again " + user);
    } else {
        user = prompt("Please enter your name:", "");
        if (user != "" && user != null) {
            setCookie("username", user, 365);
        }
    }
}


