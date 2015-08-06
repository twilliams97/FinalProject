// $( document.body ).click(function() {
//   if ( $( "li:first ).is( ":hidden" ) ) {
//     $( ".anni" ).show( "slow" );
//   } else {
//     $( ".anni" ).slideUp();
//   }
// // });
//
// $(document).ready(function()
//   $( "#clickme" ).click(function() {
//     $( "#anni" ).slideDown( "slow", function() {
//     });
//   });


$(document).ready(function(){
  $( "#clickme" ).click(function() {
    $( this ).css({
      borderStyle: "inset",
      cursor: "wait"
    });
    $( "#anni" ).slideDown( 1000, function() {
      $( "#clickme" ).css( "visibility", "hidden" );
    });
  })
});

$(document).ready(function(){
    $("#scholarship").hover(function(){
        $(this).text("More Money!!!");
        }, function(){
        $(this).text("Scholarships!");
    });
});
