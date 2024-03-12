let SpanUsername = document.getElementById('username');
let inputUsername = document.getElementById('input-username')
let usernamePencil = document.getElementById('edit-pencil-username');
let confirmUsername = document.getElementById('username-confirm');
let photoChanger = document.getElementById('photoChanger');
let DivPerfilTab = document.getElementById('perfil-controller');
let DivNewChatTab = document.getElementById('new-chat-tab');

const Api = new ApiCommunicator(window.location.href)

function updateElements() {
    SpanUsername = document.getElementById('username');
    inputUsername = document.getElementById('input-username')
    usernamePencil = document.getElementById('edit-pencil-username');
    confirmUsername = document.getElementById('username-confirm');
    photoChanger = document.getElementById('photoChanger');
    DivPerfilTab = document.getElementById('perfil-controller');
    DivNewChatTab = document.getElementById('new-chat-tab');
}

document.getElementById('search-profiles').addEventListener('input', filterProfiles);

function filterProfiles() {
    var input = document.getElementById('search-profiles');
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


function toggleTab(tab) {

    if (tab == 'profile') {
        if (DivPerfilTab.style.left === "0px") {
            DivPerfilTab.style.left = "-400px";

        } else {
            DivPerfilTab.style.left = "0px";

            SpanUsername.style.display = 'inline'
            inputUsername.style.display = 'none'
            confirmUsername.style.display = 'none'
            usernamePencil.style.display = 'inline'
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
    usernamePencil.style.display = 'none'

    inputUsername.value = SpanUsername.textContent;

    SpanUsername.style.display = 'none'
    inputUsername.style.display = 'inline'

    inputUsername.focus()
    inputUsername.addEventListener("keyup", function (event) {

        if (event.key === "Enter") {
            usernameUpdate()
        }
    })
}

function usernameUpdate() {

    SpanUsername.style.display = 'inline'
    inputUsername.style.display = 'none'
    confirmUsername.style.display = 'none'
    usernamePencil.style.display = 'inline'

    var endpoint = `api/profile/${profileID}/`;
    var data = { username: inputUsername.value }
    if (SpanUsername.textContent != inputUsername.value) {
        Api.patchData(endpoint, data)
        SpanUsername.textContent = inputUsername.value
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


    var url = `api/profile/${profileID}/`;
    await Api.profilePictureUpdate(url, arquivo)

    await updateHtmlContent('#perfil-picture')
    await updateHtmlContent('#main-header')
    // photoChanger = document.getElementById('photoChanger');

}


async function startChat(profile1ID, profile2ID) {
    var endpoint = 'api/newChatRoom/';
    var data = { profile1_id: profile1ID, profile2_id: profile2ID }
    await Api.postData(endpoint, data)

    await updateHtmlContent('#perfil-controller')
}

async function openRoom(id) {
    console.log('abrindo room')
    var endpoint = `api/chatrooms/${id}/view_messages/`
    var chatData = await Api.getData(endpoint)



    // Adicionando um campo de carimbo de data/hora às mensagens
    chatData.messages.forEach(message => {
        message.timestamp = new Date(message.timestamp);
    });

    // Ordenando as mensagens por data/hora
    chatData.messages.sort((a, b) => a.timestamp - b.timestamp);

    // Separando mensagens por remetente
    const myMessages = [];
    const otherPersonMessages = [];

    chatData.messages.forEach(message => {
        if (message.sender === chatData.chatroom.members[0].id) {
            myMessages.push(message);
        } else {
            otherPersonMessages.push(message);
        }
    });

    // Exibindo mensagens separadas
    console.log("Minhas mensagens:", myMessages);
    console.log("Mensagens da outra pessoa:", otherPersonMessages);

    // Separar o que são meus dados e o que são dados de quem eu estou conversando
}


function sendMessage(id) {
    //vai mandar menssagem pra room
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

        updateElements()
    } catch (error) {
        console.error('Erro ao atualizar conteúdo HTML:', error);
        alert('Erro ao atualizar conteúdo HTML');
    }
}
