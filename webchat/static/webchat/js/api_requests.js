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

async function requestAPI(method, url, data = "", token = "", type = 'JSON') {

    var send
    var contentType
    if (type == 'JSON') {
        if (data) {
            var requestOptions = {
                method: method,
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Token ${token}`,
                    'X-CSRFToken': csrf
                },

                body: JSON.stringify(data)
            };
        } else {
            var requestOptions = {
                method: method,
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Token ${token}`,
                    'X-CSRFToken': csrf
                },
            };
        }

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




    return fetch(url, requestOptions)
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
            return data
        })
        .catch(error => {
            console.error('Erro:', error);
        });

}



class ApiCommunicator {
    constructor(url) {
        this.baseURL = url
    }


    #getOptions() {
        return {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': this.#getApiToken(),
                'X-CSRFToken': this.#getCSRFToken(),
            },
        };
    }

    #options(method, data) {
        return {
            method: method,
            headers: {
                'Content-Type': 'application/json',
                'Authorization': this.#getApiToken(),
                'X-CSRFToken': this.#getCSRFToken(),
            },
            body: JSON.stringify(data)
        };
    }



    async getChatData(endpoint) {
        const url = `${this.baseURL}${endpoint}`;
        const options = this.#getOptions()

        try {
            const response = await fetch(url, options);
            if (!response.ok) {
                throw new Error('Erro ao fazer a solicitação à API');
            }
            const data = await response.json();
            console.log('Resposta da API:', data);
            return data;
        } catch (error) {
            console.error('Erro:', error.message);
            throw error;
        }

    }

    async usernameUpdate(endpoint, data) {
        const url = `${this.baseURL}${endpoint}`;
        const options = this.#options('PATCH', data)

        try {
            await fetch(url, options)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Erro ao fazer a solicitação à API');
                    }
                    return response.json();
                })
                .then(data => {
                    console.log('Resposta da API:', data);
                    return data
                })
        } catch (error) {
            console.error('Erro:', error.message);
            throw error;
        }

    }


    #getCSRFToken() {
        const cookies = document.cookie.split(';');
        for (const cookie of cookies) {
            const [name, value] = cookie.trim().split('=');
            if (name === 'csrftoken') {
                return value;
            }
        }
        return null;
    }

    async #getApiToken() {
        try {
            const response = await fetch(this.baseURL + 'getToken/', { method: 'GET' });
            if (!response.ok) {
                throw new Error('Erro ao obter token da API');
            }
            const data = await response.json();
            return data.token;

        } catch (error) {
            console.error('Erro ao obter token:', error);
            throw error;
        }
    };

}

