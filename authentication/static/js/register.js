async function handleFormSubmit() {
    event.preventDefault();
    let username = document.getElementById('username').value;
    let password = document.getElementById('password').value;
    let country = document.getElementById('country').value;
    register(username, password, country).then(response => {
        if (response.status == 200) {
            window.location.href = '/auth/login';
        } else {
            document.getElementById('register-fail-msg').classList.remove('hidden')
        }
    })
}

function register(username, password, country) {
    return fetch('api/register', {
        method: 'POST',
        body: JSON.stringify({
            username,
            password,
            'negara_asal': country,
        }),
    })
}