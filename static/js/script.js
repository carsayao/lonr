var start = Date.now();

function getTime() {
    return (Date.now() - start) / 1000;
};

var socket = io();

socket.on('my_response', (data, cb) => {
    console.log(getTime(), 'my_response', data);
    if (cb)
        console.log("executing cb");
        cb();
    console.log("NOT executing cb");
});

socket.on('message', data => {
    console.log(getTime(), 'client data', data);
    $('#chat-messages').prepend("<p>"+ "<strong>" + data.username
                              + ": </strong>" + data.text + "</p>");
});

socket.on('clientDisconnect', data => {
    console.log(getTime(), 'clientDisconnect');
    $('#chat-messages').prepend("<p>" + "disconnect" + "</p>");
});

$('#submit').on('click', () => {
    if ($("input[type='radio']:checked").attr('id') == undefined) {
        $('#chat-messages').prepend("<p><strong>Error: </strong>Select a guest!</p>");
        return;
    }
    console.log(getTime(), 'who', $("input[type='radio']:checked").attr('id'));
    console.log(getTime(), 'message', $('#message').val());
    $("#chat-messages").prepend("<p>" + "<strong>You: </strong>" + $('#message').val()) + "</p>"; // NOTE: Could be a bug here, parens
    socket.emit('message', {
      'strWho': $("input[type='radio']:checked").attr('id'),
      'strQuery': $('#message').val()
    });
    console.log(getTime(), 'click');
    $('#message').val('');  // Clear field
  })
;

$('.input-group').keypress( (event) => {
  if (event.keyCode == 13) {
    console.log(getTime(), "'enter' pressed");
    event.preventDefault();
    $('#submit').click();
  }
});

