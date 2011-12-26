/* Author: Thomas Levine

*/
$(function(){
  var chainsaw=['perluette','thomaslevine.com'].join('@');
  document.getElementById("e-post").innerHTML=chainsaw;
  $('.not-ie #card').hide().css('visibility','inherit').fadeIn('slow');
});
