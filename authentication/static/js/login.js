async function handleFormSubmit(event) {
    event.preventDefault();
    let username = document.getElementById('username').value;
    let password = document.getElementById('password').value;
    console.log("ini username " + username)
    console.log('ini password' + password)
    console.log('ini csrf' + document.getElementsByName("csrfmiddlewaretoken")[0].value)
    login(username, password).then(response => {
        console.log(response.json())
        if (response.ok) {
            window.location.href = '/fakhri-hijau/tayangan';
        }
    })
    
}

function login(username, password) {
    return fetch('api/login', {
        method: 'POST',
        body: JSON.stringify({
            username,
            password,
        }),
        credentials: 'same-origin',
        headers: {
            "X-CSRFToken": document.getElementsByName("csrfmiddlewaretoken")[0].value
        },
    })
}