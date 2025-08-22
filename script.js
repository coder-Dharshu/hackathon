document.addEventListener('DOMContentLoaded', function() {
    // We add a message box element to the login and register pages to display messages.
    // If you haven't already, add this line of code inside the respective containers:
    // <p id="message-box" style="margin-bottom: 15px; text-align: center;"></p>
    const messageBox = document.getElementById('message-box');
    
    // Listen for form submissions on both pages
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');

    // Handle login form submission if it exists
    if (loginForm) {
        loginForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            fetch('http://127.0.0.1:5000/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password })
            })
            .then(response => response.json())
            .then(data => {
                if (data.message === "Login successful!") {
                    messageBox.style.color = 'green';
                    messageBox.textContent = 'Login successful! Redirecting...';
                    console.log('Login successful!', data);
                    
                    // Redirect based on the user's role
                    if (data.role === 'artist') {
                        window.location.href = 'artist_dashboard.html';
                    } else {
                        // For customers, redirect to the customer dashboard
                        window.location.href = 'customer_dashboard.html';
                    }

                } else {
                    messageBox.style.color = 'red';
                    messageBox.textContent = data.error;
                    console.error('Login failed:', data.error);
                }
            })
            .catch(error => {
                messageBox.style.color = 'red';
                messageBox.textContent = 'An error occurred during login. Please check your server.';
                console.error('Network or server error:', error);
            });
        });
    }

    // Handle registration form submission if it exists
    if (registerForm) {
        registerForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            const role = document.getElementById('role').value;

            fetch('http://127.0.0.1:5000/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password, role })
            })
            .then(response => response.json())
            .then(data => {
                if (data.message === "Artist registered successfully!") {
                    messageBox.style.color = 'green';
                    messageBox.textContent = 'Registration successful! You can now log in.';
                    console.log('Registration successful!', data);
                } else {
                    messageBox.style.color = 'red';
                    messageBox.textContent = data.error;
                    console.error('Registration failed:', data.error);
                }
            })
            .catch(error => {
                messageBox.style.color = 'red';
                messageBox.textContent = 'An error occurred during registration. Please check your server.';
                console.error('Network or server error:', error);
            });
        });
    }
});
