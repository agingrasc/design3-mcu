console.log("yeah");

function goto_position() {
    var x_position = document.getElementById("x");
    var y_position = document.getElementById("y");
    console.log(x_position.value);
    console.log(y_position.value);
    $.post("http://localhost:12345/go-to-position", function(data, status) {
            data = "{'x':" + x_position.value + ",'y':" + y_position.value + " }";
        })
        .done(function() {
            alert("second success");
        })
        .fail(function(err) {
            console.log(err);
        });
}
