function getCookie(name) {
  if (!document.cookie) {
      return null;
    }

  const xsrfCookies = document.cookie.split(';')
    .map(c => c.trim())
    .filter(c => c.startsWith(name + '='));

  if (xsrfCookies.length === 0) {
      return null;
    }
  return decodeURIComponent(xsrfCookies[0].split('=')[1]);
}

function validateFields(formObj){
    const fields = formObj.querySelectorAll("[required]");
    let errors = true;
    for (i = 0; i < fields.length; i++) {
        if(!fields[i].value){
            // Marcar o field em vermelho
            errors = false;
        }
    }
    return errors
}
