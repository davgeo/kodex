/* ---------------------------------------------------
    JavaScript/jQuery
    Controls for kodi file browser
   --------------------------------------------------- */

// GET url and update filebrowser with response
function buttonControlFilebrowser(id) {
  $(id).click(function() {
    var url = this.href;
    var targetpath = $(this).attr('class');
    var prevpathlist = $('#file-browser').data('source');

    var currentpath = prevpathlist.pop();
    var prevpath = prevpathlist.pop();

    var pathhistory;
    if(targetpath == prevpath) {
      pathhistory = prevpathlist.pop();
    } else {
      pathhistory = currentpath;
    }

    pathid = { 'targetpath': targetpath,
                'pathhistory': pathhistory};
    $.get(url, pathid, function(data) {
      $(".filebrowser-wrapper").replaceWith(data);
      refreshButtonControl()

      if(targetpath != prevpath) {
        if(prevpath != undefined) {
          prevpathlist.push(prevpath);
        }

        if(currentpath != undefined) {
          prevpathlist.push(currentpath);
        }
      } else {
        prevpathlist.push(pathhistory);
      }

      prevpathlist.push(targetpath);
    });
    return false;
  });
}

// GET url and update file details with response
function buttonControlFiledetails(id) {
  $(id).click(function() {
    var url = this.href;
    var targetfile = $(this).attr('class');

    fileid = { 'targetfile': targetfile};
    $.get(url, fileid, function(data) {});
    return false;
  });
}

// GET url and update playlist with response
function buttonControlFilePlaylist(id) {
  $(id).click(function() {
    var url = this.href;
    var targetfile = $(this).attr('class');
    fileid = { 'targetfile': targetfile};
    $.get(url, fileid, function(data) {
      updatePlaylist(data);
    });
    return false;
  });
}

// GET url, update playlist with response and switch icon
function buttonControlFilePlaylistIcon(id, iconId, hasIconA, toIconB) {
  $(id).click(function() {
    var url = this.href;
    var targetfile = $(this).attr('class');
    var icon = $(iconId).find('.fa')
    fileid = { 'targetfile': targetfile};
    $.get(url, fileid, function(data) {
      updatePlaylist(data);
      if($(icon).hasClass(hasIconA)) {
        toggleIcon(icon, hasIconA, toIconB);
      }
    });
    return false;
  });
}

function refreshButtonControl() {
  buttonControlFilebrowser(".filebrowserselect a");
  buttonControlFiledetails(".filedetailselect a");
  buttonControlFilePlaylist(".addfileplaylist a"); // Add to playlist
  buttonControlFilePlaylistIcon(".playfileplaylist a", '.playercontrol.playpause', 'fa-play', 'fa-pause'); // Play item
}

/* Execute processes after page DOM is ready */
$(function() {
  buttonControlFilebrowser(".filesourceselect a")
  refreshButtonControl()
  $('#file-browser').data('source', [])
});
