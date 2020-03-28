var start = Date.now();

// Timestamp for debug
function getTime() {
  return (Date.now() - start) / 1000;
};

// var objectSocket = io.connect('http://robochat.appspot.com');
var objectSocket = io.connect('http://localhost:8080/');
// var objectSocket = io.connect('http://localhost:8080/', () => {
// 	console.log(getTime(), "objectSocket");
// });

objectSocket.on('message', function (objectData) {
    // console.log('client objectData', objectData);
    console.log(getTime(), 'client objectData', objectData);
    $('#chat-messages')
    .prepend("<p>" + "<strong>" + objectData.username + ": </strong>" + objectData.text + "</p>")
    ;
    });

objectSocket.on('clientDisconnect', function(objectData) {
    // console.log('clientDisconnect');
    console.log(getTime(), 'clientDisconnect');
    $('#chat-messages')
    .prepend("<p>" + "disconnect" + "</p>")
    ;
    });

$('#submit')
.on('click', function () {
    if ($("input[type='radio']:checked").attr('id') == undefined) {
    $('#chat-messages')
    .prepend("<p><strong>Error: </strong>Select a guest!</p>");
    return;
    }
    // console.log('who', $("input[type='radio']:checked").attr('id'));
    // console.log('message', $('#message').val());
    console.log(getTime(), 'who', $("input[type='radio']:checked").attr('id'));
    console.log(getTime(), 'message', $('#message').val());
    $("#chat-messages").prepend("<p>" + "<strong>You: </strong>" + $('#message').val()) + "</p>";
    objectSocket.emit('message', {
        'strWho': $("input[type='radio']:checked").attr('id'),
        'strQuery': $('#message').val()
        });
    // console.log('click');
    console.log(getTime(), 'click');
    // Clear field
    $('#message').val('');
    })
;

$('.input-group').keypress( (event) => {
    if (event.keyCode == 13) {
    // console.log("'enter' pressed");
    console.log(getTime(), "'enter' pressed");
    event.preventDefault();
    $('#submit').click();
    }
    });

