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

/* === SUBMIT REVIEW === */

/**
 * Send review data to API
 */
async function submitReview(token, placeId, reviewText, rating) {
    const response = await fetch(`${API_URL}/reviews/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
            text: reviewText,
            rating: parseInt(rating),
            place_id: placeId,
            user_id: getUserIdFromToken(token)
        })
    });
    return response;
}

/**
 * Decode JWT token to get user ID
 */
function getUserIdFromToken(token) {
    try {
        const payload = token.split('.')[1];
        const decoded = JSON.parse(atob(payload));
        return decoded.sub;
    } catch (err) {
        return null;
    }
}

/**
 * Setup review form event listener
 */
document.addEventListener('DOMContentLoaded', () => {
    const reviewForm = document.getElementById('review-form');
    const token = checkAuthentication();
    const placeId = getPlaceIdFromURL();

    if (!reviewForm || !token || !placeId) return;

    reviewForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const reviewText = document.getElementById('review-text').value.trim();
        const rating = document.getElementById('rating').value;

        if (!reviewText) {
            document.getElementById('error-message').textContent = 'Please enter a review.';
            return;
        }

        try {
            const response = await submitReview(token, placeId, reviewText, rating);
            handleResponse(response, reviewForm);
        } catch (err) {
            document.getElementById('error-message').textContent = 'Connection error. Please try again.';
        }
    });
});
