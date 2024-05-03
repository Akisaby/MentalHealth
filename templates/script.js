document.getElementById('loginForm').addEventListener('submit', function(event) {
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;
    var usernameError = document.getElementById('usernameError');
    var passwordError = document.getElementById('passwordError');
    
    usernameError.innerHTML = '';
    passwordError.innerHTML = '';

    if (username.trim() === '') {
        usernameError.innerHTML = 'Please enter your username.';
        event.preventDefault();
    }

    if (password.trim() === '') {
        passwordError.innerHTML = 'Please enter your password.';
        event.preventDefault();
    }
});
