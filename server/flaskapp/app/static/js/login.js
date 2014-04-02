      var authRes
      (function() {
       var po = document.createElement('script'); po.type = 'text/javascript'; po.async = true;
       po.src = 'https://apis.google.com/js/client:plusone.js';
       var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(po, s);
     })();

console.log(window.location.pathname)

  renderGButton()


function renderGButton(){
      var po = document.createElement('script'); po.type = 'text/javascript'; po.async = true;
       po.src = 'https://apis.google.com/js/client:plusone.js?onload=render';
       var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(po, s);

}

var first_run = false;
$(document).ready(function() {
$('#nav-logout').on('click',logout);
});


function loginFinishedCallBack(authResult){
    var loggedInCookie = getCookie("loggedIn")
    if (authResult['code']) {
      //console.log(authResult)
      authRes = authResult
    // Hide the sign-in button now that the user is authorized, for example:
    $('#signinButton').attr('style', 'display: none');
    gapi.client.load('plus','v1', getInfo);  // Trigger request to get the email address.

  } else if (authResult['error']) {
    console.log("error " + authResult['error'])
    if(authResult['error'] == 'user_signed_out'){
      xmlhttp = new XMLHttpRequest();
      xmlhttp.open("POST","/logout")
      xmlhttp.send();
      window.location.href="/logout"

    }
    // There was an error.
    // Possible error codes:
    //   "access_denied" - User denied access to your app
    //   "immediate_failed" - Could not automatially log in the user
    // console.log('There was an error: ' + authResult['error']);
  }

}

function render() {

  // Additional params
  var additionalParams = {
    'theme' : 'dark'
  };

  gapi.signin.render('myButton', additionalParams);
  
}

function loginHelper(auth){
      loginFinishedCallBack(auth);
}


function getInfo(){
 var request = gapi.client.plus.people.get({ 'userId': 'me'});
 request.execute(getProfileCallBack);
}

function logout(){
  console.log("logout hit");
  gapi.auth.signOut();
}


function getCookie(cname)
{
var name = cname + "=";
var ca = document.cookie.split(';');
for(var i=0; i<ca.length; i++) 
  {
  var c = ca[i].trim();
  if (c.indexOf(name)==0) return c.substring(name.length,c.length);
  }
return "";
}

function setCookie(cname,cvalue,exdays)
{
var d = new Date();
d.setTime(d.getTime()+(exdays*24*60*60*1000));
var expires = "expires="+d.toGMTString();
document.cookie = cname + "=" + cvalue + "; " + expires;
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
  //$("#nav-login").html("<a href='#'> <img src='https://plus.google.com/s2/photos/profile/" + profile.id + "?sz=25' />" + name + "</a>")
  }


