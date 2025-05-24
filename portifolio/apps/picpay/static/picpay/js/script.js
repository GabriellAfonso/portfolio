const Api = new ApiCommunicator(window.location.origin)
const myModal = new bootstrap.Modal(document.getElementById('myModal'))
let TransactionMsg = document.getElementById('error-transaction')



const transactionTab = document.getElementById("transactionTab")

function toggleTab(tab) {

    if (tab == 'transaction') {
        if (transactionTab.style.left === "0px") {
            transactionTab.style.left = "-100%";
            document.getElementById('cpfcnpj').value = '';
            document.getElementById('valueTransactionInput').value = '';


        } else {
            transactionTab.style.left = "0px";
        }
    }



}
var options = {

    onKeyPress: function (cpf, ev, el, op) {
        var masks = ['000.000.000-000', '00.000.000/0000-00'];
        $('#cpfcnpj').mask((cpf.length > 14) ? masks[1] : masks[0], op);
    }

}

$('#cpfcnpj').length > 11 ? $('#cpfcnpj').mask('00.000.000/0000-00', options) : $('#cpfcnpj').mask('000.000.000-00#', options);

function get_data_for_transaction(doc) {
    const url = `${window.location.origin}/picpay/api/start_transaction/?document=${encodeURIComponent(doc)}`;
    console.log(window.location.origin)
    fetch(url)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                var errorMessage = document.getElementById('error-transaction')
                errorMessage.textContent = data.error;
                errorMessage.style.display = 'block';
            } else {
                confirmTransaction(data.name)

            }
        })
        .catch(error => {
            console.error('Fetch error:', error);
        });
}

function startTransaction() {

    TransactionMsg.textContent = '';
    TransactionMsg.style.display = 'none';
    const receiverDocument = document.getElementById('cpfcnpj').value;
    const transactionValue = document.getElementById('valueTransactionInput').value;

    if (receiverDocument.length < 11) {

        TransactionMsg.textContent = 'Documento invalido!';
        TransactionMsg.style.display = 'block';
        return
    }


    if (transactionValue <= 0 || !validateValue(transactionValue)) {

        TransactionMsg.textContent = 'Valor invalido!';
        TransactionMsg.style.display = 'block';
        return
    }


    get_data_for_transaction(receiverDocument);
}

function validateValue(valor) {
    const regex = /^[0-9.,]*$/;
    return regex.test(valor);
}

async function transaction() {
    const receiverDocument = document.getElementById('cpfcnpj').value;
    const transactionValue = document.getElementById('valueTransactionInput').value;

    var endpoint = '/picpay/api/transaction/'

    var data = {
        document: receiverDocument,
        value: transactionValue,
    }
    var request = await Api.postData(endpoint, data)

    if (request.error) {
        transactionError(request.error)
    }
    if (request.success) {
        transactionSuccess(request.success)
        document.getElementById('cpfcnpj').value = ''
        document.getElementById('valueTransactionInput').value = ''
    }
    updateHtmlContent('#balanceValue')
    updateHtmlContent('#transactionHistory')
    myModal.hide();

}

$("#valueTransactionInput").maskMoney({ thousands: '.', decimal: ',' });

document.addEventListener('DOMContentLoaded', (event) => {
    // Crie uma instância da modal

});

function confirmTransaction(name) {
    const Value = document.getElementById('valueTransactionInput').value;
    const modalBody = document.querySelector('#myModal .modal-body p');
    modalBody.textContent = `Deseja transferir R$: ${Value} para ${name}`;

    myModal.show();

}

function transactionError(error) {
    TransactionMsg.textContent = error;
    TransactionMsg.style.display = 'block';
    TransactionMsg.style.color = '#dc3545';
}
function transactionSuccess(success) {
    TransactionMsg.textContent = success;
    TransactionMsg.style.display = 'block';
    TransactionMsg.style.color = '#198754';
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

    } catch (error) {
        console.error('Erro ao atualizar conteúdo HTML:', error);
        alert('Erro ao atualizar conteúdo HTML');
    }
}
