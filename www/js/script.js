/* Author: Thomas Levine

*/
$(function(){
  var chainsaw=['perluette','thomaslevine.com'].join('@');
  document.getElementById("e-post").innerHTML=chainsaw;
  $('.social a').click(function(){
    var thelink=$(this).attr('href');
    _gaq.push(['_trackEvent', 'Social', 'Clickthrough',thelink]);
  });
  $('div.name,div.e-post,div.phone,div.logo').click(function(){
    var theclass=$(this).attr('class');
    _gaq.push(['_trackEvent', 'Static', 'Click',theclass]);
  });
  $('#card').hide().css('visibility','inherit').fadeIn('slow');
});
