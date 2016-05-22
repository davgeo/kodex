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