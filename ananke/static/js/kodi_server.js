/* ------ */
/* jQuery */
/* ------ */

/* Execute processes after page DOM is ready */
$(function() {
  /* Main page button controls */
  buttonControlToggle(".watched a", 'fa-check-square-o', 'fa-square-o'); // Watched
  buttonControlPlaylist(".addplaylist a"); // Add to playlist
  buttonControlPlaylistIcon(".playplaylist a", '.playercontrol.playpause', 'fa-play', 'fa-pause'); // Play item
});















