      var authRes
      (function() {
       var po = document.createElement('script'); po.type = 'text/javascript'; po.async = true;
       po.src = 'https://apis.google.com/js/client:plusone.js';
       var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(po, s);
     })();


function loginFinishedCallBack(authResult){
    if (authResult['code']) {
      //console.log(authResult)
      authRes = authResult
    // Hide the sign-in button now that the user is authorized, for example:
    $('#signinButton').attr('style', 'display: none');
    gapi.client.load('plus','v1', getInfo);  // Trigger request to get the email address.

    // Send the code to the server

 // xmlhttp = new XMLHttpRequest();
 // xmlhttp.open("POST","http://localhost:8080/login?storeToken="+authResult['code'],true);
 // xmlhttp.send();
  } else if (authResult['error']) {
    // There was an error.
    // Possible error codes:
    //   "access_denied" - User denied access to your app
    //   "immediate_failed" - Could not automatially log in the user
    // console.log('There was an error: ' + authResult['error']);
  }

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
  $("#nav-login").html("<a href='#'> <img src='https://plus.google.com/s2/photos/profile/" + profile.id + "?sz=25' />" + name + "</a>");
  }


