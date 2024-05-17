async function handleFormSubmit(event) {
    event.preventDefault();
    let username = document.getElementById('username').value;
    let password = document.getElementById('password').value;
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
    })
}