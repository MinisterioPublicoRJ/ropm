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
