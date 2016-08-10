/* ---------- */
/* JavaScript */
/* ---------- */
function updateNavURL(id, prev_server, server) {
  var url = $(id).attr("href");
  $(id).attr("href", url.replace(prev_server, server));
}

/* ------ */
/* jQuery */
/* ------ */
/* Execute processes after page DOM is ready */
$(function() {
  var current_server_select;

  if($(".navbar-server-select").val() == null) {
    current_server_select = '0'
  } else {
    current_server_select = $(".navbar-server-select").val().toString();
  }

  $(".navbar-server-select").change(function() {
    var server = $(".navbar-server-select").val().toString();
    var url = document.URL + "_setserver_" + server;

    // Update navbar links
    updateNavURL("#kodi-navbar-overview-link", current_server_select, server);
    updateNavURL("#kodi-navbar-tv-link", current_server_select, server);
    updateNavURL("#kodi-navbar-movie-link", current_server_select, server);

    // Enable navbar links
    $(".kodi-navbar-button").removeClass("disabled");

    // Load control panel
    console.log(url);
    $.get(url, function(data){
      $(".control-panel-wrapper").replaceWith(data);
      InitialiseControlPanel();
    })

    current_server_select = server;
  });
});
