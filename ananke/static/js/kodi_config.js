/* ---------- */
/* JavaScript */
/* ---------- */

/* ------ */
/* jQuery */
/* ------ */
// Ping server control
function serverPing(id) {
  var button = id;
  var icon = $(".serverstatusicon", id);
  var url = id.value;

  statusButtonToggle(2, icon, button);

  $.get(url, function(){
    statusButtonToggle(1, icon, button); // Success
  }).fail(function() {
    statusButtonToggle(3, icon, button); // Fail
  });
}

/* Execute processes after page DOM is ready */
$(function() {
  // Server status button onclick control
  var server_status_button_list = document.getElementsByClassName('serverstatusbutton');
  for (var i = 0; i < server_status_button_list.length; ++i) {
    var server_status_button = server_status_button_list[i];
    serverPing(server_status_button);
  }

  $(".serverstatusbutton").click(function() {
    serverPing(this);
  });
});
