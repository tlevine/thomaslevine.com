/* Author: Thomas Levine

*/
$(function(){
  var chainsaw=['perluette','thomaslevine.com'].join('@');
  document.getElementById("e-post").innerHTML=chainsaw;
  $('.not-ie .card').each(function(i){
    $(this).delay(1000*i).hide().css('visibility','inherit').fadeIn('slow');
  });
});
