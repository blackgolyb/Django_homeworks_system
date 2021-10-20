function ajaxSend(url, method, params) {
    // Отправляем запрос

    fetch(`${url}?${params}`, {
        method: method,
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
    })
        .then(response => response.json())
        .then(json => returnJson(json))
        .catch(error => console.error(error))
}

function ajaxSendForm(form) {
  let url = form.action;
  let method = form.method;
  console.log(url, method);
  let params = new URLSearchParams(new FormData(form)).toString();
  // console.log(params);
  ajaxSend(url, method, params);
}
