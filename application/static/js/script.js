//
// EventListener for Conversations
//

const conversationElements = document.getElementsByClassName('convo');

const clearMessages = () => {
  console.log('CLEARING')
  const pageElement = document.querySelector('#main-chat-wrap');
  while (pageElement.firstChild) {
    pageElement.removeChild(pageElement.firstChild)
  }
}

const setActive = (conversation) => {
  for (element of conversationElements) {
    element.classList.remove('active')
  }
  conversation.classList.add('active')
} 

const clearChatNamefromHeader = () => {
  const headerElement = document.querySelector('.header-chat-name')
  while (headerElement.firstChild) {
    headerElement.removeChild(headerElement.firstChild)
  }
}

const addChatNametoHeader = (chatname) => {
  const headerElement = document.querySelector('.header-chat-name')
  let chatnameHeader = document.createElement('p');
  chatnameHeader.id = "header-chat-name";
  console.log(chatname)
  chatnameHeader.innerHTML = chatname
  headerElement.appendChild(chatnameHeader);
}

const updateMessages = () => {
    const activechat = document.querySelector('.active');
    // console.log(activechat)
    const chat_id = activechat.dataset.chat_id;

    if (chat_id == null) {
      return;
    } else {
      retrieveMessages(chat_id);
    }
}

setInterval(updateMessages, 1000)

const convoClick = (event) => {
  const clicked = event.currentTarget;
  if (clicked.classList.contains('active')) {
    console.log("Already active element")
  } else {
    // console.log(clicked.dataset);
    setActive(clicked);
    clearMessages();
    const dataAttributes = clicked.dataset;
    console.log(dataAttributes)
    const chat_id = dataAttributes.chat_id;
    document.querySelector('#sndr-chat_id').value = chat_id;
    retrieveMessages(dataAttributes.chat_id);
    clearChatNamefromHeader();
    addChatNametoHeader(dataAttributes.chat_name);
  }
}

for(element of conversationElements) {
    element.addEventListener('click', convoClick, false);
}

const addMessage = (currentmessage, oldmessage=true) => {
    const pageElement = document.querySelector('#main-chat-wrap');

    let messageDiv = document.createElement('div');
    messageDiv.classList.add('message-wrap');

    let messageIo = document.createElement('div');
    messageIo.classList.add('message')

    if (currentmessage["sender_id"] == document.querySelector('#sndr-name').value) {
      messageIo.classList.add('out')
      } else {
        messageIo.classList.add('in')
    }

    let messageContent = document.createElement('p');
    messageContent.classList.add('mssg');
    messageContent.innerHTML = currentmessage.content;

    let messageTime = document.createElement('p');
    messageTime.classList.add('mssg-time');
    messageTime.innerHTML = currentmessage.timesent;

    let messagePointer = document.createElement('div');
    messagePointer.classList.add('mssg-pointer');

    if (oldmessage) {
      pageElement.appendChild(messageDiv);
      } else {
        pageElement.insertBefore(messageDiv, pageElement.firstChild)
      }

    messageIo.appendChild(messageContent, messageTime);
    messageDiv.appendChild(messageIo, messagePointer);
}

const addMessages = (messages) => {
  // console.log(messages)
  clearMessages()
  messages.forEach(message => addMessage(message))
}

const retrieveMessages = (chat_id) => {
  const url = `/api/chats/${chat_id}/messages`
  console.log(`${url}`)
  fetch(url, {
      method: 'GET'
  }).then(result => result.json())
     .then(data => addMessages(data))
}


//
// Sending Messages
//

const submitNewMessage = () => {

  const newMessage = document.querySelector('#new-message').value;
  const chat_id = document.querySelector('#sndr-chat_id').value;
  const user_id = document.querySelector('#sndr-name').value;

  const url = `/api/chats/${chat_id}/messages`

  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      'content': newMessage
    })
  })
  .then(result => result.json())
  .then(data => {
    addMessage(data, oldmessage=false)
    document.querySelector('#new-message').value = '';
  })
}


// 
// Chat Modal 
// 

// Get the modal
const chatmodal = document.getElementById("newChatModal");

// Get the button that opens the modal
const chatbtn = document.getElementById("open-chat-modal-button");

// Get the <span> element that closes the modal
const chatspan = document.getElementsByClassName("chatclose")[0];

// When the user clicks the button, open the modal 
chatbtn.onclick = function() {
  chatmodal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
chatspan.onclick = function() {
  chatmodal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  console.log("clicked off")
  if (event.target == chatmodal) {
    chatmodal.style.display = "none";
  }
}


// 
// Creating a New Chat 
// 

const createChat = (chatName) => {
  const chaturl = "/api/"

  return fetch(chaturl, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      'chatname': chatName,
    })
  }).then(res => res.json());
}

const addRecipient = (chat_id, username) => {
  const chataddusrurl = `/api/${chat_id}/users`
  return fetch(chataddusrurl, {
    method: "POST",
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      'username': username
    })
  }).then(res => res.json())
}

const createNewChat = () => {
  const newChat = document.querySelector('#new_chat_name').value;
  console.log(newChat);
  const recipient_id = document.querySelector('#new_chat_recipient').value;
  console.log(recipient_id);
  createChat(newChat)

    .then(chat => chat['chat_id'])
    .then(chat_id => addRecipient(chat_id, recipient_id));

    chatmodal.style.display = "none";
}


// 
// Profile Modal 
// 

// Get the modal
const profilemodal = document.getElementById("profileModal");

// Get the button that opens the modal
const profilebtn = document.getElementById("open-profile-modal-button");

// Get the <span> element that closes the modal
const profilespan = document.getElementsByClassName("profileclose")[0];

// When the user clicks the button, open the modal 
profilebtn.onclick = function() {
  profilemodal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
profilespan.onclick = function() {
  profilemodal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == profilemodal) {
    console.log("clicked off")
    profilemodal.style.display = "none";
  }
}

// 
// Log Out 
// 

const logUserOut = () => {
  logouturl = `/logout/`
    fetch(logouturl, {
      method: 'GET',
  }).then(window.location.reload(true))     
}
