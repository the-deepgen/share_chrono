var callback_received = [];
var callback_text = [];

$(document).ready(function () {
    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/' + key);


    //receive details from server
    socket.on('new_callback', function (msg) {
        console.log("Received callback");
        callback_received.push(msg.document_id + ' | ' + msg.file_name);
        callback_text.push("Request UUID: " + msg.request_uuid + "<br>Version: " + msg.version + "<br>Index: " + msg.index);
        let callback_string = '<ul class="list-group">';
        for (let i = 0; i < callback_received.length; i++) {
            callback_string += '<li class="list-group-item list-group-item-action" data-index="' + i + '">' + callback_received[i].toString() + '</li>';
        }
        callback_string += '</ul>'
        $('#log').html(callback_string);
        $('#counter').html(callback_received.length.toString());
    });

    $("#reset").click(function () {
        console.log("Reset callback list")
        callback_received = [];
        $('#log').html("");
        $('#counter').html(0);
    });

    $('body').on('click', 'li', function () {
        let index = parseInt($(this).attr("data-index"));
        $("#extract_text").html(callback_text[index]);
        $('#extract_text_modal').modal('show');
    });
});
