async function handleFormSubmit(event) {
    event.preventDefault();
    let username = document.getElementById('username').value;
    let password = document.getElementById('password').value;
    login(username, password).then(response => {
        if (response.status == 200) {
            window.location.href = '/fakhri-hijau/tayangan';
        } else if (response.status = 401) {
            document.getElementById('login-fail-msg').classList.remove('hidden')
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
    })
}