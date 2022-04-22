console.log('ffffffffffff')
$(document).ready(function () {
    $("#submit").click(
        function () {
            var str;
            var messageData = document.getElementById('text');
            if (messageData != null) { str = messageData.textContent } else { str = null };
            var lst = String(document.location.href).split('/');
            var id = lst[4];
            createMessage('#messages-form', str, `{{ current_user.id }}`, id);
            document.getElementById('text').innerHtml = '';
            return false;
        }
    );
});

function start() {
    var str;
    var messageData = document.getElementById('text');
    if (messageData != null) { str = messageData.textContent } else { str = null };
    var lst = String(document.location.href).split('/');
    var id = lst[4];
    getMessages('#messages-form', `{{current_user.id}}`, id);
    var div = $("#messages-form");
    div.scrollTop(div.prop('scrollHeight'));

};

function createMessage(result_form, str, sender, recipient) {
    $.ajax({
        url: `http://127.0.0.1:5000/api/messages?content=${str}&sender_id=${sender}&recipient_id=${recipient}`, //url страницы (action_ajax_form.php)
        type: "post", //метод отправки
        dataType: "html", //формат данных
        success: function (response) { //Данные отправлены успешно
            getMessages(result_form, sender, recipient);
            return true;
        }
    });



};

function getMessages(result_form, sender, recipient) {
    $.ajax({
        url: `http://127.0.0.1:5000/api/messages?sender_id=${sender}&recipient_id=${recipient}`,
        type: 'get',
        dataType: 'html',
        success: function (response) {
            result = $.parseJSON(response);
            messages = result['messages'];
            outputMessage(messages, result_form);

        }
    })
};

function outputMessage(array1, result_form) {
    var lst = String(document.location.href).split('/');
    var id = lst[4];
    var output_form = document.querySelector(result_form);
    output_form.innerHTML = '';
    array1.forEach(function (value) {
        if (value['recipient_id'] == id) {
            var template = document.querySelector('#messages-template');
        }
        else {
            var template = document.querySelector('#own-messages-template');
        };



        var clone = template.content.cloneNode(true);
        var content_place = clone.querySelector('#messages-content');
        var time_place = clone.querySelector('#messages-get-time');

        var message = value['content'];
        var send_time = value['send_time'];

        var text = document.createTextNode(message);
        var time = document.createTextNode(send_time);


        time_place.appendChild(time);
        content_place.appendChild(text);
        output_form.appendChild(clone);

    });
    window.scrollTo(0, document.body.scrollHeight);

};
start();
