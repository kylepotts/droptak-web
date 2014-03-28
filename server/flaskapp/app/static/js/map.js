var start = 4
var mapName
$(document).ready(function()  { $('.carousel').carousel({ interval: 4000, cycle: true }); });
$(document).ready(function() {
$('#addMap').on('click',onAddMapClick);
$('#view_map_link').on('click', onViewMapClick)
});

function onAddMapClick(e){
    console.log("click");
    mapName = getMapName()
    $('#items').append("\
                                <div class='col-sm-3'> \
                            <div class='col-item'> \
                                <div class='photo'> \
                                    <img src='http://maps.googleapis.com/maps/api/staticmap?center=Brooklyn+Bridge,New+York,NY&zoom=13&size=350x260&maptype=roadmap\
&markers=color:blue%7Clabel:S%7C40.702147,-74.015794&markers=color:green%7Clabel:G%7C40.711614,-74.012318\
&markers=color:red%7Clabel:C%7C40.718217,-73.998284&sensor=false' class='img-responsive' alt='a' /> \
                                </div>\
                                <div class='info'>\
                                    <div class='row'>\
                                        <div class='price col-md-6'>\
                                            <h5>"+mapName+"\
                                                </h5>\
                                            <h5 class='price-text-color'>\
                                                Location</h5>\
                                        </div>\
                                        <div class='rating hidden-sm col-md-6'>\
                                        </div>\
                                    </div>\
                                    <div class='separator clear-left'>\
                                        <p class='btn-add'>\
                                            <i class='fa fa-shopping-cart'></i><a href='http://www.jquery2dotnet.com' class='hidden-sm'>Add to cart</a></p>\
                                        <p class='btn-details'>\
                                            <i class='fa fa-list'></i><a href='http://www.jquery2dotnet.com' class='hidden-sm'>More details</a></p>\
                                    </div>\
                                    <div class='clearfix'>\
                                    </div>\
                                </div>\
                            </div>\
                        </div>");
  xmlhttp = new XMLHttpRequest();
  xmlhttp.open("POST","http://mapitapps.appspot.com//maps/new?name="+mapName)
  xmlhttp.send();
}


function onViewMapClick(e){
    console.log("onViewMapClicked")
}

function getMapName(){
    name = $('#mapName').val()
    console.log(name)
    return name
}



