function loadDialogs() {
    const promise = getDialogs();
    promise.then(data => {
        showDialogs(data)
    })
}

function showDialogs(data) {
    var dialogsInf = data['data']['dialogs'];
    var cur_user = data['data']['user_id'];

    dialogsInf.forEach(function (dialog) {
        const outputForm = document.querySelector('#dialogs-output');
        const templateToast = document.querySelector('#dialog-message-box');
        const clone = templateToast.content.cloneNode(true);

        const timeAgoPlace = clone.querySelector('#time-ago-strong');
        const dialogLast = clone.querySelector('#last-message-text');
        const userName = clone.querySelector('#user-name-text');

        var recipient_id;
        if (cur_user == dialog['user_one_id']) {
            var recipient_id = dialog['user_two_id']
        }
        else {
            var recipient_id = dialog['user_one_id']
        };



        const namePromise = getUser(recipient_id);
        namePromise.then(userData => {

            var user = userData['data']['users'];
            var userNameVal = user['name'];
            var userSurnameVal = user['surname'];

            var fullName = document.createTextNode(`${userNameVal} ${userSurnameVal}`);
            userName.appendChild(fullName);


        });

        const lastMessagePromise = getMessages(recipient_id);
        lastMessagePromise.then(messagesData => {
            var messagesList = messagesData['data']['messages'][0];
            console.log(messagesList);
            if ((messagesList != undefined) && (Object.keys(messagesList).length > 1)) {
                var messageText = messagesList['content'];
                var messageTime = messagesList['send_time'];
                console.log(messageTime)
                var date = messageTime.split(' ')[0].split('-');
                var time = messageTime.split(" ")[1].split(':');
                var dateTime = new Date(`${date[0]}-${date[1]}-${date[2]}T${time[0]}:${time[1]}`)
                var nowTime = new Date();
                var timeDelta = nowTime - dateTime;
                var timeAgo = Math.round(timeDelta / 86400000);
                var col = 'day(s)'
                if (timeAgo < 1) {
                    var timeAgo = Math.round(timeDelta / 36000000);
                    var col = 'hour(s)'
                    if (timeAgo < 1) {
                        var timeAgo = Math.round(timeDelta / 60000)
                        var col = 'minute(s)'
                    }
                }
                var lastMessageTimeAgo = timeAgo + ` ${col}`

                var timeAgoNode = document.createTextNode(lastMessageTimeAgo);
                var lastMessage = document.createTextNode(messageText);
                dialogLast.appendChild(lastMessage);
                timeAgoPlace.appendChild(timeAgoNode);

            };
        });
        const div = clone.getElementById('dialogs-div');

        div.onclick = function () {
            document.location.href = `http://127.0.0.1:5000/dialogs/${recipient_id}`
        }
        console.log(div.href)
        outputForm.appendChild(clone);

    })
}


function showMessages() {
    const messagesPromise = getMessages(id = 0, count = 0);
    messagesPromise.then(messagesData => {
        console.log(messagesData)
        var curUser = messagesData['data']['user_id']
        var messagesList = messagesData['data']['messages']
        const outputForm = document.querySelector('#messages-form')
        messagesList.forEach(message => {
            var messageText = message['content']
            var sendTime = message['send_time'];

            if (message['recipient_id'] == id) {
                var template = document.querySelector('#messages-template');
            }
            else {
                var template = document.querySelector('#own-messages-template');
            };
            const clone = template.content.cloneNode(true);
            const contentPlace = clone.querySelector('#messages-content');
            const timePlace = clone.querySelector('#messages-get-time');

            var text = document.createTextNode(messageText);
            var time = document.createTextNode(sendTime);

            

            timePlace.appendChild(time);
            contentPlace.appendChild(text);
            outputForm.appendChild(clone);

        })
        outputForm.scrollTop = outputForm.scrollHeight
        
    })
};

$(document).ready(function () {
    $("#message-send-submit").click(function () {
        var messageData = document.querySelector('#text');
        if (messageData.textContent != null) {
            str = messageData.textContent;
            postMessage(str);
        }
    })
});
function postMessage(messageText) {
    const messagePromise = sendMessage(messageText)
    messagePromise.then(data => {showMessages()})
};