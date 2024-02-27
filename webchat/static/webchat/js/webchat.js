const SpanUsername = document.getElementById('username');
const inputUsername = document.getElementById('input-username')
const usernamePencil = document.getElementById('edit-pencil-username');
const confirmUsername = document.getElementById('username-confirm');

const photoChanger = document.getElementById("photoChanger");

const DivPerfilTab = document.getElementById('perfil-controller');
const DivNewChatTab = document.getElementById('new-chat-tab');



const token = $.ajax({
    url: window.location.href + 'get-token/',
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
        profileApiEdit('PATCH', url, data, token)
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
    profileApiEdit('PATCH', url, arquivo, token, 'PHOTO')
}