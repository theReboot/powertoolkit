$(".scrollTo").click(function(o){console.log("scrollTo Clicked");var l=$(this).attr("href"),t=$(l).offset();$("html, body").stop().animate({scrollTop:t.top},500),o.preventDefault()});