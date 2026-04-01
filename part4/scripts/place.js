/* === PLACE DETAILS PAGE === */

const API_URL = 'http://localhost:5000/api/v1';

/**
 * Extract place ID from URL query parameters
 */
function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id');
}

/**
 * Fetch place details from API
 */
async function fetchPlaceDetails(token, placeId) {
    try {
        const headers = { 'Content-Type': 'application/json' };
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const response = await fetch(`${API_URL}/places/${placeId}`, { headers });

        if (!response.ok) {
            throw new Error('Place not found');
        }

        const place = await response.json();
        displayPlaceDetails(place);
    } catch (err) {
        const placeDetails = document.getElementById('place-details');
        if (placeDetails) {
            placeDetails.innerHTML = '<p class="error-message">Failed to load place details.</p>';
        }
    }
}

/**
 * Display place details dynamically
 */
function displayPlaceDetails(place) {
    const placeDetails = document.getElementById('place-details');
    if (!placeDetails) return;

    placeDetails.innerHTML = `
        <h1>${place.title}</h1>
        <div class="place-info">
            <span>🏠 Host: ${place.owner.first_name} ${place.owner.last_name}</span>
            <span>💰 Price: $${place.price} / night</span>
            <span>📍 Location: ${place.latitude}, ${place.longitude}</span>
            <span>⭐ Amenities: ${place.amenities.map(a => a.name).join(', ') || 'None'}</span>
        </div>
        <p class="description">${place.description || ''}</p>
    `;

    // Display reviews
    const reviewsList = document.getElementById('reviews-list');
    if (reviewsList) {
        if (place.reviews && place.reviews.length > 0) {
            reviewsList.innerHTML = '';
            place.reviews.forEach(review => {
                const card = document.createElement('div');
                card.className = 'review-card';
                card.innerHTML = `
                    <p class="rating">${'⭐'.repeat(review.rating)}</p>
                    <p class="author">By: ${review.user_id}</p>
                    <p>${review.text}</p>
                `;
                reviewsList.appendChild(card);
            });
        } else {
            reviewsList.innerHTML = '<p>No reviews yet.</p>';
        }
    }
}

/* === ADD REVIEW ACCESS === */

/**
 * Show or hide add review section based on authentication
 * and add link to add_review.html with place ID
 */
function checkAuthForReview(token, placeId) {
    const addReviewSection = document.getElementById('add-review');

    if (!addReviewSection) return;

    if (token) {
        addReviewSection.style.display = 'block';

        // Update form action to include place ID
        const reviewForm = document.getElementById('review-form');
        if (reviewForm) {
            reviewForm.dataset.placeId = placeId;
        }

        // Add link to add_review page
        const addReviewLink = document.createElement('a');
        addReviewLink.href = `add_review.html?id=${placeId}`;
        addReviewLink.className = 'details-button';
        addReviewLink.textContent = 'Write a Review';
        addReviewSection.appendChild(addReviewLink);
    } else {
        addReviewSection.style.display = 'none';
    }
}

/**
 * Initialize place details page
 */
document.addEventListener('DOMContentLoaded', () => {
    const placeId = getPlaceIdFromURL();
    const token = getCookie('token');

    if (!placeId) {
        window.location.href = 'index.html';
        return;
    }

    fetchPlaceDetails(token, placeId);
    checkAuthForReview(token, placeId);
});
