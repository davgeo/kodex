/* Javascript */

function volumeControl() {
  var x = document.getElementById("myslider").value;
  var url = document.URL + "_setvolume_" + x.toString()
  console.log(x);
  var xhttp = new XMLHttpRequest();
  xhttp.open("GET", url, true);
  xhttp.send();
}
