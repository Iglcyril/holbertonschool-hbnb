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
