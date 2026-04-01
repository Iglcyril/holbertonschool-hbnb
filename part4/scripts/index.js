/* === INDEX PAGE === */

const API_URL = 'http://localhost:5000/api/v1';
let allPlaces = [];

/**
 * Check authentication and fetch places on page load
 */
document.addEventListener('DOMContentLoaded', () => {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');

    if (!token) {
        if (loginLink) loginLink.style.display = 'block';
    } else {
        if (loginLink) loginLink.style.display = 'none';
    }

    // Fetch places regardless of authentication
    fetchPlaces(token);

    // Setup price filter
    const priceFilter = document.getElementById('price-filter');
    if (priceFilter) {
        priceFilter.addEventListener('change', (event) => {
            filterPlacesByPrice(event.target.value);
        });
    }
});
