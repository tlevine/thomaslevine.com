/* Author: Thomas Levine

*/
$(function(){
  _gaq.push(['_setCustomVar',1,'Generated email address',chainsaw]);
  $('.social a').click(function(){
    var thelink=$(this).attr('href');
    _gaq.push(['_trackEvent', 'Social', 'Clickthrough',thelink]);
  });
});
