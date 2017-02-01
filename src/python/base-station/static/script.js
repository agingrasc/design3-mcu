console.log("yeah")
function goto_position(){
    $.get("http//localhost:12345/goto_position", function(data, status){
        alert("Data: " + data + "\nStatus: " + status);
    });
    alert("Go To Position")
}
