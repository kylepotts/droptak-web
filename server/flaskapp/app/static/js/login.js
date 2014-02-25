      (function() {
       var po = document.createElement('script'); po.type = 'text/javascript'; po.async = true;
       po.src = 'https://apis.google.com/js/client:plusone.js';
       var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(po, s);
     })();


function loginFinishedCallBack(authResult){
  if (authResult) {
    if (authResult['error'] == undefined){
        document.getElementById('signinButton').setAttribute('style', 'display: none'); // Hide the sign-in button after successfully signing in the user.
        gapi.client.load('plus','v1', getInfo);  // Trigger request to get the email address.
      } else {
        console.log('An error occurred');
      }
  } else {
      console.log('Empty authResult');  // Something went wrong
    }
  }


function getInfo(){
 var request = gapi.client.plus.people.get({ 'userId': 'me'});
 request.execute(getProfileCallBack);
}


function getProfileCallBack(obj){
  profile = obj;
  console.log(profile)
  email = obj['emails'].filter(function(v) {
        return v.type === 'account'; // Filter out the primary email
    })[0].value;
  name = obj['displayName'];
  console.log("Email: " + email);
  console.log("Name: "+ name);
  xmlhttp = new XMLHttpRequest();
  xmlhttp.open("POST","http://mapitapps.appspot.com/login?name="+name+"&email="+email,true);
  xmlhttp.send();
  $("#nav-login").html("<a href='#'> <img src='https://plus.google.com/s2/photos/profile/" + profile.id + "?sz=25' />" + name + "</a>");
  }



