/* === COOKIE HELPERS === */

/**
 * Set a cookie with a name, value and expiration in days
 */
function setCookie(name, value, days) {
    const expires = new Date();
    expires.setTime(expires.getTime() + (days * 24 * 60 * 60 * 1000));
    document.cookie = `${name}=${value}; expires=${expires.toUTCString()}; path=/`;
}

/**
 * Get a cookie value by its name
 */
function getCookie(name) {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [cookieName, cookieValue] = cookie.trim().split('=');
        if (cookieName === name) {
            return cookieValue;
        }
    }
    return null;
}

/**
 * Delete a cookie by its name
 */
function deleteCookie(name) {
    document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/`;
}

/**
 * Check if user is authenticated
 */
function isAuthenticated() {
    return getCookie('token') !== null;
}

/**
 * Update navigation based on authentication status
 * Shows/hides login link and adds logout button if authenticated
 */
function updateNavigation() {
    const loginLink = document.getElementById('login-link');

    if (isAuthenticated()) {
        if (loginLink) loginLink.style.display = 'none';

        // Add logout button if not already present
        if (!document.getElementById('logout-btn')) {
            const nav = document.querySelector('nav');
            const logoutBtn = document.createElement('button');
            logoutBtn.id = 'logout-btn';
            logoutBtn.textContent = 'Logout';
            logoutBtn.className = 'login-button';
            logoutBtn.addEventListener('click', () => {
                deleteCookie('token');
                window.location.href = 'login.html';
            });
            nav.appendChild(logoutBtn);
        }
    } else {
        if (loginLink) loginLink.style.display = 'block';
    }
}

// Run on every page load
document.addEventListener('DOMContentLoaded', updateNavigation);

/* === LOGIN === */

/**
 * Send login request to API
 */
async function loginUser(email, password) {
    const response = await fetch('http://localhost:5000/api/v1/auth/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
    });
    return response;
}

/**
 * Handle login form submission
 */
document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const email = document.getElementById('email').value.trim();
            const password = document.getElementById('password').value.trim();
            const errorMessage = document.getElementById('error-message');

            try {
                const response = await loginUser(email, password);

                if (response.ok) {
                    const data = await response.json();
                    setCookie('token', data.access_token, 7);
                    window.location.href = 'index.html';
                } else {
                    const error = await response.json();
                    errorMessage.textContent = error.message || 'Login failed. Please check your credentials.';
                }
            } catch (err) {
                errorMessage.textContent = 'Connection error. Please try again.';
            }
        });
    }
});
