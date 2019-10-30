// console.log(mockAPI.myInfo.myName)

// const setHeaderImage = () => {
//     const pageElement = document.querySelector('#self-image');
//     let imageElement = document.createElement('img');
//     imageElement.classList.add('icon-img');
//     imageElement.setAttribute('src', `images/${mockAPI.myInfo.icon}`);
//     imageElement.setAttribute('alt', "Puppy Icon Image for " + mockAPI.myInfo.myName)
//     console.log(imageElement)
//     pageElement.appendChild(imageElement)
// }

const addMessage = (currentmessage) => {
    const pageElement = document.querySelector('#main-chat-wrap');

    let messageDiv = document.createElement('div');
    messageDiv.classList.add('message-wrap');

    let messageIo = document.createElement('div');
    messageIo.classList.add('message')
    messageIo.classList.add(currentmessage.sent ? 'out' : 'in')

    let messageContent = document.createElement('p');
    messageContent.classList.add('mssg');
    messageContent.innerHTML = currentmessage.content;

    let messageTime = document.createElement('p');
    messageTime.classList.add('mssg-time');
    messageTime.innerHTML = currentmessage.timesent;

    let messagePointer = document.createElement('div');
    messagePointer.classList.add('mssg-pointer');

    messageIo.appendChild(messageContent, messageTime);
    messageDiv.appendChild(messageIo, messagePointer);
    pageElement.appendChild(messageDiv);
}

const addAllMessageElements = () => {
    for (currentmessage of mockAPI.conversations[0].messages){
        console.log(`Working on ${currentmessage}`)
        addMessage(currentmessage);
    }
}

const conversationElements = document.getElementsByClassName('convo');

const convoClick = (event) => {
    const clicked = event.currentTarget;
    console.log(clicked.dataset)
    retrieveMessages(clicked.dataset);
}

for(element of conversationElements) {
    element.addEventListener('click', convoClick, false);
}

const retrieveMessages = (req_info) => {
    const url = `/api/chats/${req_info.chat_id}/messages?user_id=${req_info.user_id}`
    fetch(url, {
        method: 'GET'
    }).then(result => result.json())
       .then(data => addMessages(data))
}

const addMessages = (messages) => {
    // console.log(messages)
    messages.forEach(message => addMessage(message))
}
