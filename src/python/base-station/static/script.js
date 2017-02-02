console.log("yeah")
function goto_position(){
    var x_position = document.getElementById("x");
    var y_position = document.getElementById("y");
    console.log(x_position.value);
    console.log(y_position.value);
    $.get("http://localhost:12345/go-to-position", function(data, status){
        })
        .done(function() {
            alert( "second success" );
        })
        .fail(function() {
            alert( "error" );
    });
}
