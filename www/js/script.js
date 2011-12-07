/* Author: Thomas Levine

*/
$(function(){
  var chainsaw=['perluette','thomaslevine.com'].join('@');
  document.getElementById("e-post").innerHTML=chainsaw;
  $('.social a').click(function(){
    var thelink=$(this).attr('href');
    _gaq.push(['_trackEvent', 'Social', 'Clickthrough',thelink]);
  });
});
