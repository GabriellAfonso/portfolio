class ApiCommunicator {
    constructor(url) {
        this.baseURL = url
    }


    async send(url, options) {
        try {
            const response = await fetch(url, options);
            if (!response.ok) {
                throw new Error('Erro ao fazer a solicitação à API');
            }
            const data = await response.json();
            // console.log('Resposta da API:', data);
            return data;
        } catch (error) {
            console.error('Erro:', error.message);
            throw error;
        }
    }


    #options(method, data, includeContentType = true) {
        const headers = {
            'Authorization': this.#getApiToken(),
            'X-CSRFToken': this.#getCSRFToken(),
        };

        if (includeContentType) {
            headers['Content-Type'] = 'application/json';
        }

        const options = {
            method: method,
            headers: headers,
        };

        if (data) {
            if (includeContentType) {
                options.body = JSON.stringify(data)
            } else {
                var formData = new FormData();
                formData.append("profile_picture", data);
                options.body = formData
            }

        }

        return options;
    }



    async getData(endpoint) {
        const url = `${this.baseURL}${endpoint}`;
        const options = this.#options('GET', null)
        return await this.send(url, options)
    }

    async postData(endpoint, data) {
        const url = `${this.baseURL}${endpoint}`;
        const options = this.#options('POST', data)
        return await this.send(url, options)

    }

    async patchData(endpoint, data) {
        const url = `${this.baseURL}${endpoint}`;
        const options = this.#options('PATCH', data);
        return await this.send(url, options)
    }


    async profilePictureUpdate(endpoint, picture) {
        const url = `${this.baseURL}${endpoint}`;
        const options = this.#options('PATCH', picture, false)
        console.log(options)

        return await this.send(url, options)
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

