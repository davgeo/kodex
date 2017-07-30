/* ---------------------------------------------------
    JavaScript/jQuery
    Controls for kodi navbar
   --------------------------------------------------- */

function updateNavURL(id, prev_server, server) {
  var url = $(id).attr("href");
  $(id).attr("href", url.replace(prev_server, server));
}

/* Execute processes after page DOM is ready */
$(function() {
  var current_server_select;

  if($(".navbar-server-select").val() == null) {
    current_server_select = '0'
  } else {
    current_server_select = $(".navbar-server-select").val().toString();
  }

  $(".navbar-server-select").change(function() {
    if($(".kodi-navbar-server-url").length) {
      var url = $(this, ".kodi-navbar-server-url").val().toString();
      console.log(url);
      window.location.replace(url);
    } else {
      var server = $(".navbar-server-select").val().toString();
      var url = document.URL + "_setserver_" + server;

      // Update navbar links
      updateNavURL("#kodi-navbar-overview-link", current_server_select, server);
      updateNavURL("#kodi-navbar-tv-link", current_server_select, server);
      updateNavURL("#kodi-navbar-movie-link", current_server_select, server);
      updateNavURL("#kodi-navbar-addon-link", current_server_select, server);
      updateNavURL("#kodi-navbar-file-link", current_server_select, server);

      updateNavURL("#kodi-navbar-togglesubtitles-link", current_server_select, server);
      updateNavURL("#kodi-navbar-cyclesubtitles-link", current_server_select, server);
      updateNavURL("#kodi-navbar-videoscan-link", current_server_select, server);
      updateNavURL("#kodi-navbar-clear-link", current_server_select, server);
      updateNavURL("#kodi-navbar-quit-link", current_server_select, server);

      // Enable navbar links
      $(".kodi-navbar-button").removeClass("disabled");
      $(".disable_href").removeClass("disabled");

      // Enable navbar playcontrol dropdown button
      $("#kodi-navbar-playcontrol-dropdown-button").removeAttr("disabled")

      // Load control panel
      console.log(url);
      $.get(url, function(data){
        $(".control-panel-wrapper").replaceWith(data);
        InitialiseControlPanel();
      })

      current_server_select = server;
    }
  });
});
