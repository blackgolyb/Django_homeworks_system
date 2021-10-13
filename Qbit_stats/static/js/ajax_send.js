function ajaxSend(url, method, params) {
    // Отправляем запрос

    fetch(`${url}?${params}`, {
        method: method,
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
    })
        .then(response => response.json())
        .then(json => render(json))
        .catch(error => console.error(error))
}
