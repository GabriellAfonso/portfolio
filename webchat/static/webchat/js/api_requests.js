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


function profileApiEdit(method, url, data, token, type) {
    const csrf = getCSRFToken()
    var send
    var contentType
    if (type == 'JSON') {
        send = JSON.stringify(data)
    } else if (type == 'PHOTO') {
        send = new FormData();
        send.append("profile_picture", data);

    }


    const requestOptions = {
        method: method,
        headers: {
            'Authorization': `Token ${token}`,
            'X-CSRFToken': csrf
        },
        body: send
    };

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

            location.reload();
        })
        .catch(error => {
            console.error('Erro:', error);
        });

}



