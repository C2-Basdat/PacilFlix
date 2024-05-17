function handleLogout() {
    fetch('/auth/api/logout', {
        method:'POST',
    }).then(response => {
        if (response.ok) {
            window.location.href = "/auth"
        }
    })
}