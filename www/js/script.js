/* Author: Thomas Levine

*/
$(function(){
  var chainsaw=['perluette','thomaslevine.com'].join('@');
  document.getElementById("e-post").innerHTML=chainsaw;
  $('.not-ie .card').each(function(i){
    $(this).delay(100*i).animate({opacity:1},'1000');
  });
});
