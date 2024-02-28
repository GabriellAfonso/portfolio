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


function requestAPI(method, url, data, token, type = 'JSON') {
    const csrf = getCSRFToken()
    var send
    var contentType
    if (type == 'JSON') {
        var requestOptions = {
            method: method,
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${token}`,
                'X-CSRFToken': csrf
            },
            body: JSON.stringify(data)
        };

    } else if (type == 'PHOTO') {
        photo = new FormData();
        photo.append("profile_picture", data);
        var requestOptions = {
            method: method,
            headers: {
                'Authorization': `Token ${token}`,
                'X-CSRFToken': csrf
            },
            body: photo
        };

    }




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
            if (type == 'PHOTO') {
                location.reload();
            }
        })
        .catch(error => {
            console.error('Erro:', error);
        });

}



