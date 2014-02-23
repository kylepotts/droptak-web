var $ = jQuery.noConflict(); 
console.log($)
$(document).ready(function()  { $('#myCarousel').carousel({ interval: 3000, cycle: true }); });