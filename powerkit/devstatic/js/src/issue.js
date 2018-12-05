$('.scrollTo').click(function(e){
  console.log("scrollTo Clicked")
  var jump = $(this).attr('href');
  var new_position = $(jump).offset();
  $('html, body').stop().animate({ scrollTop: new_position.top }, 500);
  e.preventDefault();
});

// https://developers.google.com/web/updates/2017/09/sticky-headers
// todo: add class when nav is "stuck" to top
