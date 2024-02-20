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
    $.ajax({
        type: 'GET',
        url: '/logout/',  // Substitua pela URL correta do seu endpoint de logout
        success: function (data) {
            window.location.href = "/logout/";
            console.log('Logout successful');
            // Implemente qualquer lógica adicional após o logout, como redirecionamento
        },
        error: function () {
            console.log('Logout failed');
        }
    });
}

function logoutAjax() {

}