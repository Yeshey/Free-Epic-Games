const ws = new WebSocket("ws://127.0.0.1:5678/");
var x;
console.log(ws);
send()
function send(){
    x = "Message from Browser!"
    try {
        ws.onopen = function(response){
            ws.send(x);
        };
    } catch (error) {
        console.log(error)
    }
    console.log("Msg sent ", x);
}