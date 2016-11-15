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
      buttonControlFilebrowser(".filebrowserselect a");

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

/* Execute processes after page DOM is ready */
$(function() {
  buttonControlFilebrowser(".filesourceselect a")
  buttonControlFilebrowser(".filebrowserselect a")
  $('#file-browser').data('source', [])
});
