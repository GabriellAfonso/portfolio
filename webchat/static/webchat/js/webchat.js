
function getCSRFToken() {
    const cookies = document.cookie.split(';');
    for (const cookie of cookies) {
        const [name, value] = cookie.trim().split('=');
        if (name === 'csrftoken') {
            return value;
        }
    }
    return null;
}


const csrf = getCSRFToken()

const url = window.location.href + 'api/profile/11';

const data = {
    user_name: "Gabriel Afonso"
};

const requestOptions = {
    method: 'PATCH',
    headers: {
        'Content-Type': 'application/json',
        'Authorization': "Token e9c2c4e1ccd186026f9a918f18d5ee12ca621f74",
        'X-CSRFToken': csrf
    },
    body: JSON.stringify(data)
};


function toggleTab() {

    var tabContent = document.getElementById("perfil-controller");
    if (tabContent.style.left === "0px") {
        tabContent.style.left = "-400px";


    } else {
        tabContent.style.left = "0px";
        var username = document.getElementById('username');
        var inputUsername = document.getElementById('input-username');
        var editPencil = document.getElementById('edit-pencil');
        var confirmButton = document.getElementById('confirm-button');

        username.style.display = 'inline'
        inputUsername.style.display = 'none'
        confirmButton.style.display = 'none'
        editPencil.style.display = 'inline'
    }
}

function usernameChange() {

    var username = document.getElementById('username');
    var inputUsername = document.getElementById('input-username');
    var editPencil = document.getElementById('edit-pencil');
    var confirmButton = document.getElementById('confirm-button');


    confirmButton.style.display = 'inline'
    editPencil.style.display = 'none'


    inputUsername.value = username.textContent;

    username.style.display = 'none'
    inputUsername.style.display = 'inline'


    inputUsername.focus()

}

function changeUsername() {
    var editPencil = document.getElementById('edit-pencil');
    var confirmButton = document.getElementById('confirm-button');
    confirmButton.style.display = 'none'
    editPencil.style.display = 'inline'

    fetch(url, requestOptions)
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro ao fazer a solicitação à API');
            }
            return response.json();
        })
        .then(data => {
            console.log('Resposta da API:', data);
            // Faça o que quiser com os dados da resposta da API
        })
        .catch(error => {
            console.error('Erro:', error);
        });
}

function logoutAjax() {

}