// mobile nav

function showMenu() {
  var topNav = document.getElementById("topNav");
  topNav.classList.toggle("topNav--closed");
}

$(document).ready(function() {
  $(function() {
    if(location.pathname !== '/') {
      $('.topNav a[href^="/' + location.pathname.split("/")[1] + '"]').addClass('topNav__item--active');
    }
  });
})
