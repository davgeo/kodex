/* ---------- */
/* JavaScript */
/* ---------- */

/* ------ */
/* jQuery */
/* ------ */
// Swap icon
function toggleIcon(id, toggleA, toggleB) {
  if ($(id).hasClass(toggleA)) {
    $(id).removeClass(toggleA).addClass(toggleB); }
  else if ($(id).hasClass(toggleB)) {
    $(id).removeClass(toggleB).addClass(toggleA); }
}

// Ping server control
function serverPing(id) {
  var button = id;
  var icon = $(".serverstatusicon", id);
  var url = id.value;
  console.log(url);

  // Update status button with spinning refresh
  if($(icon).hasClass('fa-question-circle')) {
    toggleIcon(icon, 'fa-question-circle', 'fa-refresh fa-spin')
  } else if($(icon).hasClass('fa-exclamation-circle')) {
    toggleIcon(icon, 'fa-exclamation-circle', 'fa-refresh fa-spin')
  } else if($(icon).hasClass('fa-check')) {
    toggleIcon(icon, 'fa-check', 'fa-refresh fa-spin')
  }

  if($(button).hasClass('btn-primary')) {
    toggleIcon(button, 'btn-primary', 'btn-warning')
  } else if($(button).hasClass('btn-danger')) {
    toggleIcon(button, 'btn-danger', 'btn-warning')
  } else if($(button).hasClass('btn-success')) {
    toggleIcon(button, 'btn-success', 'btn-warning')
  }

  $.get(url, function(){
    // Success - mark server online
    if($(icon).hasClass('fa-refresh fa-spin')) {
      toggleIcon(icon, 'fa-refresh fa-spin', 'fa-check')
    }

    if($(button).hasClass('btn-warning')) {
      toggleIcon(button, 'btn-warning', 'btn-success')
    }
  }).fail(function() {
    // Failure - mark server offline
    if ($(icon).hasClass('fa-refresh fa-spin')) {
      toggleIcon(icon, 'fa-refresh fa-spin', 'fa-exclamation-circle')
    }

    if ($(button).hasClass('btn-warning')) {
      toggleIcon(button, 'btn-warning', 'btn-danger')
    }
  });
  return false;
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
