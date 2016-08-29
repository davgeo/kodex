/* ---------------------------------------------------
    JavaScript/jQuery
    Controls for kodi control panel
   --------------------------------------------------- */

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

// Volume slider control
function volumeControl(volume) {
  var url = $("#volslider-link").attr('href');
  console.log(url, volume);
  $.get(url, data={'volume':volume});
}

// Progress bar slider control
function progressControl() {
  var x = $("#playerprogressbar").slider("value");
  var url = document.URL + "_setprogress_" + x.toString()
  console.log("Progress (Slide) %: ".concat(x));
  $.get(url);
}

function updatePlaylist(data) {
  console.log("Updated playlist");
  $(".playlist-wrapper").replaceWith(data);

  /* Configure button controls on any updates */
  buttonControlPlaylist(".playlistremove a"); // Playlist Remove
  buttonControlPlaylist(".playlistplay a"); // Playlist Play
}

var getPlaylist_running = false;

// Recursively poll for playlist updates
function getPlaylist() {
  if ($("#server-status-link").length) {
    var url = $("#server-playlist-link").attr('href');
    getPlaylist_running = true;

    $.get(url, function(data){
      updatePlaylist(data);

      // Recusive call every 60s
      setTimeout(getPlaylist, 60000);
    }).fail(function() {
      getPlaylist_running = false;
    });
  } else {
    getPlaylist_running = false;
  }
}

function getPlaylistWrapper() {
  if(!getPlaylist_running) {
    getPlaylist();
  } else {
    console.log("getPlaylist is already running");
  }
}

// GET url and update playlist with response
function buttonControlPlaylist(id) {
  $(id).click(function() {
    var url = this.href;
    console.log(url);
    $.get(url, function(data) {
      updatePlaylist(data);
    });
    return false;
  });
}

// GET url, update playlist with response and switch icon
function buttonControlPlaylistIcon(id, iconId, hasIconA, toIconB) {
  $(id).click(function() {
    var url = this.href;
    var icon = $(iconId).find('.fa')
    console.log(url);
    $.get(url, function(data) {
      updatePlaylist(data);
      if($(icon).hasClass(hasIconA)) {
        toggleIcon(icon, hasIconA, toIconB);
      }
    });
    return false;
  });
}

// GET url and close dropdown menu
function dropdownControlBasic(id) {
  $(id).click(function() {
    var url = this.href;
    console.log(url);
    $('#kodi-navbar-playcontrol-dropdown-button').dropdown('toggle');
    $.get(url);
    return false;
  });
}

// GET url, update playlist with response and close dropdown menu
function dropdownControlPlaylist(id) {
  $(id).click(function() {
    var url = this.href;
    console.log(url);
    $('#kodi-navbar-playcontrol-dropdown-button').dropdown('toggle');
    $.get(url, function(data) {
      updatePlaylist(data);
    });
    return false;
  });
}

var getStatus_running = false;

// Recursively poll for status
function getStatus() {
  var icon = $("#navbar-serverstatus-icon");
  var button = $("#navbar-serverstatus-button");

  if ($("#server-status-link").length) {
    var url = $("#server-status-link").attr('href');

    getStatus_running = true;

    statusButtonToggle(2, icon, button);

    $.get(url, function(data){
      // Progress bar
      console.log(data);
      $("#playerprogressbar").slider({value: data['percentage']});

      // Volume slider
      updateVolSlider(data['volume'])

      // Muted icon
      if(((data['muted']) && ($("#mute").hasClass('fa-volume-up'))) ||
         ((!data['muted']) && ($("#mute").hasClass('fa-volume-off')))) {
        toggleIcon("#mute", 'fa-volume-up', 'fa-volume-off');
      }

      // Play/pause icon
      if(((data['speed'] == 0) && ($("#playpause").hasClass('fa-pause'))) ||
         ((data['speed'] != 0) && ($("#playpause").hasClass('fa-play')))) {
        toggleIcon("#playpause", 'fa-play', 'fa-pause');
      }

      // Status button
      statusButtonToggle(1, icon, button);

      // Recusive call every 10s
      setTimeout(getStatus, 10000);
    }).fail(function() {
      // If getstatus failed update status button
      statusButtonToggle(3, icon, button);
      getStatus_running = false;
    });
  } else {
    var server = $(".navbar-server-select").val();
    if($(".navbar-server-select").val() == null) {
      statusButtonToggle(0, icon, button);
    } else {
      statusButtonToggle(3, icon, button);
    }
    getStatus_running = false;
  }
}

function getStatusWrapper() {
  if(!getStatus_running) {
    getStatus();
  } else {
    console.log("getStatus is already running");
  }
}

/* Initialise navbar */
function InitialiseNavbar() {
  dropdownControlPlaylist(".playlistclear a"); // Clear playlist
  dropdownControlBasic(".videolibscan a"); // Video library scan
  dropdownControlBasic(".subtitles a"); // Subtitles
}

/* Initialise control panel */
function InitialiseControlPanel() {
  // Initialise player progress bar
  $("#playerprogressbar").slider({
    orientation: "horizontal",
    max: 100,
    min: 0,
    stop: progressControl
  });

  // Status button onclick control
  $("#navbar-serverstatus-button").click(function() {
    if(!$("#navbar-serverstatus-icon").hasClass('fa-refresh')) {
      getStatusWrapper();
      getPlaylistWrapper();
    }
  });

  // Volume slider
  $("#volslider").change(function() {
    volumeControl(this.value);
  })

  // Toggle playlist button onclick control
  $("#toggleplaylist").click(function() {
    toggleIcon("#toggleplaylisticon", 'fa-chevron-up', 'fa-chevron-down');
  });

  $("#toggleplayercontrols").click(function() {
    toggleIcon("#toggleplayercontrolsicon", 'fa-chevron-up', 'fa-chevron-down');
  });

  // Disable clickability of disable links
  $(".disable_href").click(function() {
    if($(".disable_href").hasClass('disabled')) {
      return false;
    }
  });

  /* Control panel */
  buttonControlToggle(".mute a", 'fa-volume-up', 'fa-volume-off'); // Mute
  buttonControlToggle(".playpause a", 'fa-play', 'fa-pause'); // Playpause
  buttonControlPlaylistIcon(".stop a", '.playercontrol.playpause', 'fa-pause', 'fa-play'); // Stop
  buttonControlBasic(".forward a"); // Forward
  buttonControlBasic(".backward a"); // Backward
  buttonControlBasic(".restart a"); // Restard
  buttonControlPlaylist(".skip a"); // Skip

  /* Playlist button controls */
  buttonControlPlaylist(".playlistremove a"); // Playlist Remove
  buttonControlPlaylist(".playlistplay a"); // Playlist Play

  // Recursive poll for updated status
  getStatusWrapper();

  // Recursive poll for updated playlist
  getPlaylistWrapper();
}

/* Capture key press
 * Spacebar - Play/pause
 * -/+      - Decrement/increment volume
 * m        - Toggle mute
 * s        - Subtitles
 */
function InitialiseHotKeys() {
  $(document).on("keypress", function (e) {
    var focus = document.activeElement;

    if(!(focus && (focus.tagName.toLowerCase() == 'input'))) {
      console.log("KEY CODE: ".concat(e.which));
      if(e.which == 32) {
        // Spacebar
        if($("#playpause").length) {
          var url = $("#playpause-link").attr('href');
          $.get(url);
          toggleIcon("#playpause", 'fa-play', 'fa-pause');
        }
        return false;
      }
      else if((e.which == 45)||(e.which == 95)) {
        // Minus key (with or without shift)
        if($("#volslider").length) {
          volumeControl(minusVolume());
        }
        return false;
      }
      else if((e.which == 61)||(e.which == 43)) {
        // Plus key (with or without shift)
        if($("#volslider").length) {
          volumeControl(plusVolume());
        }
        return false;
      }
      else if(e.which == 109) {
        // m
        if($("#mute").length) {
          var url = $("#mute-link").attr('href');
          $.get(url);
          toggleIcon("#mute", 'fa-volume-up', 'fa-volume-off');
        }
        return false;
      }
      else if(e.which == 115) {
        // s
        if($("#kodi-navbar-togglesubtitles-link").length) {
          var url = $("#kodi-navbar-togglesubtitles-link").attr('href');
          $.get(url);
        }
        return false;
      }
    }
  });
}

/* Execute processes after page DOM is ready */
$(function() {
  InitialiseNavbar();
  InitialiseControlPanel();
  InitialiseHotKeys();
});
