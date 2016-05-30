/* ---------- */
/* JavaScript */
/* ---------- */

// Get value of volume slider
function getVolume() {
  var x = parseInt(document.getElementById("volslider").value);
  console.log("Volume: ".concat(x))
  return x;
}

// Update value of volume slider
function updateVolSlider(x) {
  document.getElementById("volslider").value = x;
}

// Decrement volume by 2
function minusVolume() {
  var x = getVolume();
  if(x > 0) {
    x = x - 2;
  }
  updateVolSlider(x);
  return x;
}

// Increment volume by 2
function plusVolume() {
  var x = getVolume();
  if(x < 100) {
    x = x + 2;
  }
  updateVolSlider(x);
  return x;
}

/* ------ */
/* jQuery */
/* ------ */

// Volume slider control
function volumeControl() {
  var url = document.URL + "_setvolume_" + getVolume().toString()
  $.get(url);
}

// Swap icon
function toggleIcon(id, toggleA, toggleB) {
  if ($("#".concat(id)).hasClass(toggleA)) {
    $("#".concat(id)).removeClass(toggleA).addClass(toggleB); }
  else if ($("#".concat(id)).hasClass(toggleB)) {
    $("#".concat(id)).removeClass(toggleB).addClass(toggleA); }
}

/* Capture key press
 * Spacebar - Play/pause
 * -/+      - Decrement/increment volume
 * m        - Toggle mute
 */
$(document).on("keypress", function (e) {
  console.log("KEY CODE: ".concat(e.which));
  if(e.which == 32) {
    // Spacebar
    var url = document.URL + "_playpause";
    $.get(url);
    toggleIcon("playpause", 'fa-play', 'fa-pause');
    return false;
  }
  else if((e.which == 45)||(e.which == 95)) {
    // Minus key (with or without shift)
    var url = document.URL + "_setvolume_" + minusVolume().toString();
    $.get(url);
    return false;
  }
  else if((e.which == 61)||(e.which == 43)) {
    // Plus key (with or without shift)
    var url = document.URL + "_setvolume_" + plusVolume().toString();
    $.get(url);
    return false;
  }
  else if(e.which == 109) {
    // m
    var url = document.URL + "_mute";
    $.get(url);
    toggleIcon("mute", 'fa-volume-up', 'fa-volume-off');
    return false;
  }
});

// Progress bar slider control
function progressControl() {
  var x = $("#playerprogressbar").slider("value");
  var url = document.URL + "_setprogress_" + x.toString()
  console.log("Progress (Slide) %: ".concat(x));
  $.get(url);
}

// Recursively poll for status
function getStatus() {
  var url = document.URL + "_getstatus"

  // Update status button with spinning refresh
  if($("#statusicon").hasClass('fa-exclamation-circle')) {
    toggleIcon("statusicon", 'fa-exclamation-circle', 'fa-refresh fa-spin')
  }

  if($("#statusbutton").hasClass('btn-danger')) {
    toggleIcon("statusbutton", 'btn-danger', 'btn-warning')
  }

  $.get(url, function(data){
    // Progress bar
    console.log(data)
    $("#playerprogressbar").slider({value: data['percentage']});

    // Volume slider
    updateVolSlider(data['volume'])

    // Muted icon
    if(((data['muted']) && ($("#mute").hasClass('fa-volume-up'))) ||
       ((!data['muted']) && ($("#mute").hasClass('fa-volume-off')))) {
      toggleIcon("mute", 'fa-volume-up', 'fa-volume-off');
    }

    // Play/pause icon
    if(((data['speed'] == 0) && ($("#playpause").hasClass('fa-pause'))) ||
       ((data['speed'] != 0) && ($("#playpause").hasClass('fa-play')))) {
      toggleIcon("playpause", 'fa-play', 'fa-pause');
    }

    // Status button
    if($("#statusicon").hasClass('fa-refresh fa-spin')) {
      toggleIcon("statusicon", 'fa-refresh fa-spin', 'fa-check')
    }

    if($("#statusbutton").hasClass('btn-warning')) {
      toggleIcon("statusbutton", 'btn-warning', 'btn-success')
    }

    // Recusive call every 10s
    setTimeout(getStatus, 10000);
  }).fail(function() {
    // If getstatus failed update status button
    if($("#statusicon").hasClass('fa-check')) {
      toggleIcon("statusicon", 'fa-exclamation-circle', 'fa-check')
    } else if ($("#statusicon").hasClass('fa-refresh fa-spin')) {
      toggleIcon("statusicon", 'fa-refresh fa-spin', 'fa-exclamation-circle')
    }

    if($("#statusbutton").hasClass('btn-success')) {
      toggleIcon("statusbutton", 'btn-danger', 'btn-success')
    } else if ($("#statusbutton").hasClass('btn-warning')) {
      toggleIcon("statusbutton", 'btn-warning', 'btn-danger')
    }
  });
}

/* Execute processes after page DOM is ready */
$(function() {

  // Initialise player progress bar
  $("#playerprogressbar").slider({
    orientation: "horizontal",
    max: 100,
    min: 0,
    stop: progressControl
  });

  // Status button onclick control
  $("#statusbutton").click(function() {
    if($("#statusicon").hasClass('fa-exclamation-circle')) {
      getStatus();
    }
  });

  // Toggle playlist button onclick control
  $("#toggleplaylist").click(function() {
    toggleIcon("toggleplaylisticon", 'fa-chevron-up', 'fa-chevron-down');
  });

  $("#toggleplayercontrols").click(function() {
    toggleIcon("toggleplayercontrolsicon", 'fa-chevron-up', 'fa-chevron-down');
  });

  // Recursive poll for updated status
  getStatus();
});
