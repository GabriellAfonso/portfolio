const SpanUsername = document.getElementById('username');
const inputUsername = document.getElementById('input-username')
const usernamePencil = document.getElementById('edit-pencil-username');
const confirmUsername = document.getElementById('username-confirm');

const photoChanger = document.getElementById("photoChanger");

const DivPerfilTab = document.getElementById('perfil-controller');
const DivNewChatTab = document.getElementById('new-chat-tab');

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






const token = $.ajax({
    url: window.location.href + 'getToken/',
    method: 'GET',
    success: function (data) {
        return data
    }
});

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

    var url = window.location.href + `api/profile/${profileID}/`;
    var data = { user_name: inputUsername.value }
    if (SpanUsername.textContent != inputUsername.value) {
        requestAPI('PATCH', url, data, token)
        SpanUsername.textContent = inputUsername.value
    }
}

function logoutAjax() {

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

function updatePhotoProfile(input) {
    var arquivo = input.files[0];


    var url = window.location.href + `api/profile/${profileID}/`;
    requestAPI('PATCH', url, arquivo, token, 'PHOTO')

}


function startChat(p1, p2) {
    console.log(p1, ' ', p2)
    var url = window.location.href + 'api/newChatRoom/';
    var data = { profile1_id: p1, profile2_id: p2 }
    requestAPI('POST', url, data, token)

    setTimeout(function () {
        $.ajax({
            url: window.location.href,
            type: 'GET',
            success: function (data) {
                var contentToUpdate = $(data).find('#rooms').html();
                console.log(contentToUpdate)
                // Atualiza o conteúdo do elemento <div> com o novo conteúdo recebido
                $('#rooms').html(contentToUpdate);
            },
            error: function () {
                // Trata erros, se houver
                alert('Erro ao carregar novo conteúdo');
            }
        });
    }, 500)

}

async function openRoom(id) {
    try {
        // Vai dar get na room
        var url = window.location.href + `api/chatrooms/${id}/view_messages/`;

        // Faz a requisição e espera pelos dados
        var roomData = await requestAPI('GET', url);

        // Lógica para lidar com os dados recebidos da API
        console.log('------------');
        console.log(roomData);

        // Separar o que são meus dados e o que são dados de quem eu estou conversando
        var chatContent = document.getElementById("chat-content");
        chatContent.style.display = 'inline';
    } catch (error) {
        // Lidar com erros
        console.error(error);
    }
}


function sendMessage(id) {
    //vai mandar menssagem pra room
}