function getBairros(object) {
    const bairroUrl = `/v1/dados/bairros-rj/${object.value}`;
    fetch(bairroUrl, {method: "GET"})
    .then(response => response.json())
    .then(data => {
        let bairroSelector = document.querySelector("#bairro_operacao");
        bairroSelector.innerHTML = "";
        data.forEach(bairro => {
            let option = document.createElement("option");
            option.text = bairro.bairro;
            bairroSelector.add(option);
        })
    ;})
    .catch(error => {})
}

function getBatalhoes(object) {
    const batalhaoUrl = `/v1/dados/batalhoes-rj/${object.value}`;
    fetch(batalhaoUrl, {method: "GET"})
    .then(response => response.json())
    .then(data => {
        let batalhaoSelector = document.querySelector("#batalhao_operacao");
        batalhaoSelector.innerHTML = "";
        data.forEach(batalhao => {
            let option = document.createElement("option");
            option.text = batalhao.bpm;
            batalhaoSelector.add(option);
        })
    ;})
    .catch(error => {})
}

function submitInfoGeraisForm(event){
    event.preventDefault();
    let is_valid = validateFields(document.querySelector("#form-informacoes-gerais"));

    if (is_valid){
        const formUUID = document.querySelector("#form_uuid").value;
        const apiOperacoesGeraisURL = `/v1/operacoes/cria-informacoes-gerais/${formUUID}`;
        const formData = JSON.stringify({
            data: document.querySelector("#data_operacao").value,
            hora: document.querySelector("#hora_operacao").value,
            municipio: document.querySelector("#municipio_operacao").value,
            bairro: document.querySelector("#bairro_operacao").value,
            localidade: document.querySelector("#localidade_operacao").value,
            endereco_referencia: document.querySelector("#endereco_referencia").value,
            batalhao_responsavel: document.querySelector("#batalhao_operacao").value,
        });
        fetch(
            apiOperacoesGeraisURL,
        {
                method: "POST",
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie("csrftoken")
                },
                body: formData
        })
        .then(response => response.json())
        .then(data => {
            window.location = `/operacoes/cadastro/informacoes/operacionais/${formUUID}`;
        })
    }
}
