const Api = new ApiCommunicator(window.location.href)

//elements instantiated
let profileUsername = document.getElementById('username');
let inputUsername = document.getElementById('input-username')
let usernameEditPencil = document.getElementById('edit-pencil-username');
let confirmUsername = document.getElementById('username-confirm');
let photoChanger = document.getElementById('photoChanger');
let DivPerfilTab = document.getElementById('perfil-controller');
let DivNewChatTab = document.getElementById('new-chat-tab');
let messageSenderInput = document.getElementById('sender-input');
let searchProfiles = document.getElementById('search-profiles')
let searchRooms = document.getElementById('search-rooms')
let chatRoomContent = document.getElementById('chat-content');
let chatRoomName = chatRoomContent.querySelector('.chat-name span');
let chatRoomPicture = chatRoomContent.querySelector('.chat-picture img');
let chatBody = chatRoomContent.querySelector('.chat-body');

let activeRoomID = 0

setInterval(() => {
    if (activeRoomID != 0) {
        updateRoom()
    }

}, 1000)

messageSenderInput.addEventListener("keyup", function (event) {

    if (event.key === "Enter") {
        sendMessage()
    }
})


function updatePerfilElements() {
    profileUsername = document.getElementById('username');
    inputUsername = document.getElementById('input-username')
    usernameEditPencil = document.getElementById('edit-pencil-username');
    confirmUsername = document.getElementById('username-confirm');
    photoChanger = document.getElementById('photoChanger');
    DivPerfilTab = document.getElementById('perfil-controller');
}

searchProfiles.addEventListener('input', filterProfiles);
function filterProfiles() {
    var input = searchProfiles
    var filter = input.value.toUpperCase().trim();
    var profiles = document.getElementsByClassName('profiles-div');

    for (var i = 0; i < profiles.length; i++) {
        var username = profiles[i].getElementsByClassName('user-name')[0];
        var usernameText = username.textContent.toUpperCase().trim();

        if (usernameText.startsWith(filter)) {
            profiles[i].style.display = "";
        } else {
            profiles[i].style.display = "none";
        }
    }
}

searchRooms.addEventListener('input', filterRooms);
function filterRooms() {
    var input = searchRooms
    var filter = input.value.toUpperCase().trim();
    var profiles = document.getElementsByClassName('chatroom');

    for (var i = 0; i < profiles.length; i++) {
        var username = profiles[i].getElementsByClassName('chatroom-username')[0];
        var usernameText = username.textContent.toUpperCase().trim();

        if (usernameText.startsWith(filter)) {
            profiles[i].style.display = "";
        } else {
            profiles[i].style.display = "none";
        }
    }
}


function toggleTab(tab) {

    if (tab == 'profile') {
        if (DivPerfilTab.style.left === "0px") {
            DivPerfilTab.style.left = "-400px";

        } else {
            DivPerfilTab.style.left = "0px";

            profileUsername.style.display = 'inline'
            inputUsername.style.display = 'none'
            confirmUsername.style.display = 'none'
            usernameEditPencil.style.display = 'inline'
        }
    }

    if (tab == 'new-chat') {
        if (DivNewChatTab.style.left === "0px") {
            DivNewChatTab.style.left = "-400px";

        } else {
            DivNewChatTab.style.left = "0px";

        }
    }

}

function usernameEditor() {

    confirmUsername.style.display = 'inline'
    usernameEditPencil.style.display = 'none'

    inputUsername.value = profileUsername.textContent;

    profileUsername.style.display = 'none'
    inputUsername.style.display = 'inline'

    inputUsername.focus()
    inputUsername.addEventListener("keyup", function (event) {

        if (event.key === "Enter") {
            usernameUpdate()
        }
    })
}

function usernameUpdate() {

    profileUsername.style.display = 'inline'
    inputUsername.style.display = 'none'
    confirmUsername.style.display = 'none'
    usernameEditPencil.style.display = 'inline'

    var endpoint = `api/profile/${selfProfileID}/`;
    var data = { username: inputUsername.value }

    if (profileUsername.textContent != inputUsername.value) {
        Api.patchData(endpoint, data)
        profileUsername.textContent = inputUsername.value
    }
}



function showPhotoChager() {
    photoChanger.style.display = "flex";
}

function hidePhotoChager(element) {
    element.style.display = "none";
}

function changePhoto() {
    document.getElementById("input-photo").click()
}

async function updatePhotoProfile(input) {
    var arquivo = input.files[0];

    var url = `api/profile/${selfProfileID}/`;
    await Api.profilePictureUpdate(url, arquivo)

    await updateHtmlContent('#perfil-picture')
    await updateHtmlContent('#main-header')

}


async function startChat(profile1ID, profile2ID) {
    var endpoint = 'api/newChatRoom/';
    var data = { profile1_id: profile1ID, profile2_id: profile2ID }
    await Api.postData(endpoint, data)

    await updateHtmlContent('#perfil-controller')
}


function scrollToBottom() {
    chatBody.scrollTop = chatBody.scrollHeight;
}



async function openRoom(room_id) {
    activeRoomID = room_id
    await updateRoom()
    scrollToBottom()
}


async function updateRoom() {

    var endpoint = `api/chatrooms/${activeRoomID}/view_messages/`
    var chatData = await Api.getData(endpoint)


    var roomMembers = chatData.chatroom.members
    var roomMessages = chatData.messages

    roomMessages = formatMessageDates(roomMessages)
    roomMessages = groupMessagesByDay(roomMessages)

    clearChatBody()
    await chatRoomCostructor(roomMembers, roomMessages)

}


function groupMessagesByDay(roomMessages) {
    const groupedMessages = {};

    roomMessages.forEach(message => {
        const date = new Date(message.timestamp).toLocaleDateString();
        if (!groupedMessages[date]) {
            groupedMessages[date] = [];
        }
        groupedMessages[date].push(message);
    });
    return groupedMessages;
}



async function chatRoomCostructor(roomMembers, roomMessages) {
    for (const date in roomMessages) {
        displayDate(date)
        roomMessages[date].forEach(message => {
            if (message.sender === selfProfileID) {
                addSelfDivMessage(message)

            } else {
                addFriendDivMessage(message)
            }
        });
    }

    const friendINFO = getFriendInfo(roomMembers)
    chatRoomName.textContent = friendINFO.friendName;
    chatRoomPicture.src = friendINFO.friendPicture;
    chatRoomContent.style.display = 'block'
}


function displayDate(date) {
    const today = new Date().toLocaleDateString();
    const yesterday = getYesterdayDate()


    if (today == date) {
        addDateDiv('Today')
    } else if (yesterday == date) {
        addDateDiv('Yesterday')
    } else {
        addDateDiv(date)
    }
}

function getYesterdayDate() {
    const today = new Date();
    const yesterday = new Date(today);
    yesterday.setDate(today.getDate() - 1);
    return yesterday.toLocaleDateString();
}

function addDateDiv(date) {
    const Div = `
    <div class="messagesDate">
    <div class="dateBox">
      <span>${date}</span>
    </div>
  </div>`;

    chatBody.innerHTML += Div;
}
function addSelfDivMessage(message) {
    const Div = `
    <div class="myMessages">
    <div class="messageBox">
      <div class="messageText">
         <p>${message.content}</p>
      </div>
      <div class="messageTime">
        <span>${message.time}</span>
      </div>
    </div>
  </div>`;

    chatBody.innerHTML += Div;
}


function addFriendDivMessage(message) {
    const Div = `
    <div class="friendMessages">
            <div class="messageBox">
            <div class="messageText">
            <p>${message.content}</p>
            </div>
            <div class="messageTime">
              <span>${message.time}</span>
            </div>
          </div>
          </div>`;

    chatBody.innerHTML += Div;
}


function getFriendInfo(membersRoom) {
    const friendINFO = {}
    membersRoom.forEach(member => {
        if (member.id != selfProfileID) {
            friendINFO.friendPicture = member.profile_picture
            friendINFO.friendName = member.username
        }
    });
    return friendINFO
}

function formatMessageDates(roomMessages) {
    roomMessages.forEach(message => {
        message.timestamp = new Date(message.timestamp);
        var messageDate = message.timestamp
        const hour = messageDate.getHours().toString().padStart(2, '0');
        const minute = messageDate.getMinutes().toString().padStart(2, '0');
        message.time = `${hour}:${minute}`
    });

    return roomMessages
}

function clearChatBody() {
    chatBody.innerHTML = '';
}


async function sendMessage() {
    var endpoint = `api/chatrooms/${activeRoomID}/send_message/`
    var data = {
        room: activeRoomID,
        sender: selfProfileID,
        content: messageSenderInput.value
    }

    await Api.postData(endpoint, data)
    messageSenderInput.value = ''
    updateRoom()
}


async function updateHtmlContent(selector) {
    try {
        const response = await fetch(window.location.href);
        if (!response.ok) {
            throw new Error('Erro ao carregar novo conteúdo');
        }

        const htmlData = await response.text();
        const contentToUpdate = $(htmlData).find(selector).html();
        await $(selector).html(contentToUpdate);

        updatePerfilElements()
    } catch (error) {
        console.error('Erro ao atualizar conteúdo HTML:', error);
        alert('Erro ao atualizar conteúdo HTML');
    }
}
