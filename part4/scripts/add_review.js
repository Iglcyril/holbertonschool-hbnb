/* === ADD REVIEW PAGE === */

const API_URL = 'http://localhost:5000/api/v1';

/**
 * Extract place ID from URL query parameters
 */
function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id');
}

/**
 * Check authentication and redirect if not logged in
 */
function checkAuthentication() {
    const token = getCookie('token');
    if (!token) {
        window.location.href = 'index.html';
        return null;
    }
    return token;
}

/**
 * Initialize add review page
 */
document.addEventListener('DOMContentLoaded', () => {
    const token = checkAuthentication();
    const placeId = getPlaceIdFromURL();

    if (!token) return;

    if (!placeId) {
        window.location.href = 'index.html';
        return;
    }

    // Display place title if available
    const placeTitle = document.getElementById('place-title');
    if (placeTitle) {
        fetch(`${API_URL}/places/${placeId}`, {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            }
        })
        .then(res => res.json())
        .then(place => {
            placeTitle.textContent = `Place: ${place.title}`;
        })
        .catch(() => {
            placeTitle.textContent = '';
        });
    }
});
