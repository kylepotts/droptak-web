      var authRes
      (function() {
       var po = document.createElement('script'); po.type = 'text/javascript'; po.async = true;
       po.src = 'https://apis.google.com/js/client:plusone.js';
       var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(po, s);
     })();

$(document).ready(function() {
$('#nav-logout').on('click', logout)
$('#searchMapName').on('click', searchMaps);
$('#searchLocation').on('click',searchLoc);
$('#searchKeyword').on('click',searchKeyword);

});


function searchMaps(){
  var query = $('#searchBox').val();
  console.log("query="+query);
  //alert("Search for Map Name " + query)
  xmlhttp = new XMLHttpRequest();
  var qUrl = "/search?queryType=searchMaps&query="+query
  window.location.href = qUrl;
  //xmlhttp.open("GET",qUrl);
}

function searchLoc(){
  var query = $('#searchBox').val();
  alert("Search for Loc " + query);
}

function searchKeyword(){
  var query = $('#searchBox').val();
  alert("Search for Keyword " + query);
}


function loginFinishedCallBack(authResult){
  if(window.location.pathname == '/'){
    console.log("true")
    if (authResult['code']) {
      //console.log(authResult)
      authRes = authResult
    // Hide the sign-in button now that the user is authorized, for example:
    $('#signinButton').attr('style', 'display: none');
    gapi.client.load('plus','v1', getInfo);  // Trigger request to get the email address.

  } else if (authResult['error']) {
      console.log("error")

      if(authResult['error'] == "user_signed_out"){
      xmlhttp = new XMLHttpRequest();
      xmlhttp.open("POST","/logout");
      xmlhttp.send();
      alert("You are now logged out");
      window.location.href="/logoutIndex"

      }
    // There was an error.
    // Possible error codes:
    //   "access_denied" - User denied access to your app
    //   "immediate_failed" - Could not automatially log in the user
    // console.log('There was an error: ' + authResult['error']);
  }
}

}

function logout(){
  //console.log("logout click")
  //gapi.auth.signOut();
    var revokeUrl = 'https://accounts.google.com/o/oauth2/revoke?token=' +
      gapi.auth.getToken().access_token;

  // Perform an asynchronous GET request.
  $.ajax({
    type: 'GET',
    url: revokeUrl,
    async: false,
    contentType: "application/json",
    dataType: 'jsonp',
    success: function(nullResponse) {
      // Do something now that user is disconnected
      // The response is always undefined.
      xmlhttp = new XMLHttpRequest();
      xmlhttp.open("POST","/logout");
      xmlhttp.send();
      alert("You are now logged out");
      window.location.href="/"
    },
    error: function(e) {
      // Handle the error
      // console.log(e);
      // You could point users to manually disconnect if unsuccessful
      // https://plus.google.com/apps
    }
  });
}





function getInfo(){
 var request = gapi.client.plus.people.get({ 'userId': 'me'});
 request.execute(getProfileCallBack);
}


function getProfileCallBack(obj){
  profile = obj;
  console.log(authRes)
  console.log(profile)
  email = obj['emails'].filter(function(v) {
        return v.type === 'account'; // Filter out the primary email
    })[0].value;
  name = obj['displayName'];
  console.log("Email: " + email);
  console.log("Name: "+ name);
  storeToken = authRes['code']
  xmlhttp = new XMLHttpRequest();
  xmlhttp.open("POST","/login?storeToken="+storeToken+"&name="+name+"&email="+email,true);
  xmlhttp.send();
  $('#myModal').modal('hide');
  window.location.href='/dash';
  }

