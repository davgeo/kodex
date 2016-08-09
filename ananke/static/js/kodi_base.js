/* ---------- */
/* JavaScript */
/* ---------- */

/* ------ */
/* jQuery */
/* ------ */
/* Execute processes after page DOM is ready */
$(function() {
  $(".navbar-server-select").change(function() {
    var server = $(".navbar-server-select").val();
    var url = document.URL + "_setserver_" + server.toString();
    console.log(url);
    $.get(url, function(data){
      $(".control-panel-wrapper").replaceWith(data);
      InitialiseControlPanel();
    });
    /*$("a.mylink").attr("href", "http://cupcream.com");*/
  });
});
