function getCookie(name) {
  if (!document.cookie) {
    return null;
  }

  const xsrfCookies = document.cookie
    .split(";")
    .map((c) => c.trim())
    .filter((c) => c.startsWith(name + "="));

  if (xsrfCookies.length === 0) {
    return null;
  }
  return decodeURIComponent(xsrfCookies[0].split("=")[1]);
}

function validateFields(formObj) {
  const fields = formObj.querySelectorAll("[required]");
  //const progressChecked = document.querySelector(".progressbar li");

  let errors = true;
  for (i = 0; i < fields.length; i++) {
    if (!fields[i].value) {
      fields[i].style.borderColor = "#ED0606";
      //progressChecked.style.backgroundColor = "red";
      errors = false;
    } else {
      fields[i].style.borderColor = "#0676ED";
      //progressChecked.style.backgroundColor = "#4AD13B";
    }
  }
  return errors;
}

function buildFormData(fields){
    let formData = {};
    Object.entries(fields).forEach(field => {
        formData[field[0]] = document.querySelector(field[1]).value;
    });
    return JSON.stringify(formData);
}

function submitFormInfo(event){
    event.preventDefault();
    let is_valid = validateFields(document.querySelector("#main-form"));

    if (is_valid){
        const formUUID = document.querySelector("#form_uuid").value;

        const apiFullURL = API_URL + formUUID;
        const forwardFullURL = FORWARD_URL + formUUID;
        const formData = buildFormData(FORM_VAR_LIST);
        fetch(
            apiFullURL,
        {
                method: "PUT",
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie("csrftoken")
                },
                body: formData
        })
        .then(response => response.json())
        .then(data => {
            window.location = forwardFullURL;
        })
    }
}
