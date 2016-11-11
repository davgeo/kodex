/* ---------------------------------------------------
    JavaScript/jQuery
    Controls for kodi file browser
   --------------------------------------------------- */

// GET url and update filebrowser with response
function buttonControlFilebrowser(id) {
  $(id).click(function() {
    pathid = { 'dirpath': $(this).attr('class')};
    console.log(pathid);
    var url = this.href;
    $.get(url, pathid, function(data) {
      console.log("Updated file browser");
      $(".filebrowser-wrapper").replaceWith(data);
    });
    return false;
  });
}

/* Execute processes after page DOM is ready */
$(function() {
  buttonControlFilebrowser(".fileselect a")
});
