function removeTak(id){
	//send delete to server
        if (!confirm("Are you sure you want to permanently delete this tak?")) return;
        $.ajax({
            url: '/api/v1/tak/' + id,
            type: 'DELETE',
            success: function (result) {
                console.log(result);
		        window.location.reload(true);
            }
        });
}
function favoriteMap(id, mapid){
        $.ajax({
            url: '/api/v1/user/' + id + '/favorites/?mapid=' + mapid,
            type: 'POST',
            success: function (result) {
                console.log(result);
                alert("Map Favorited!");
            },
            error: function(result){
                console.log(result);
                alert("Unable to favorite map.");
            }
        });
}
