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

    // Hero background image
    const placeHero = document.querySelector('.place-hero');
    if (placeHero) {
        if (place.image_url) {
            placeHero.style.backgroundImage = `url('${place.image_url}')`;
            placeHero.style.backgroundSize = 'cover';
            placeHero.style.backgroundPosition = 'center';
        }
    }

    // Amenities badges
    const amenitiesHTML = place.amenities.length > 0
        ? place.amenities.map(a => `<span class="amenity-badge">${a.name}</span>`).join('')
        : '<span class="amenity-badge">No amenities listed</span>';

    placeDetails.innerHTML = `
        <h1>${place.title}</h1>
        <p class="place-host">Hosted by ${place.owner.first_name} ${place.owner.last_name}</p>
        <div class="place-info">
            <span>📍 ${place.latitude}, ${place.longitude}</span>
        </div>
        <p class="description">${place.description || ''}</p>
        <div class="amenities-section">
            <h3>Amenities</h3>
            <div class="amenities-list">${amenitiesHTML}</div>
        </div>
    `;

    // Price card
    const priceDisplay = document.getElementById('price-display');
    if (priceDisplay) {
        priceDisplay.innerHTML = `
            <p class="big-price">$${place.price}<span> / night</span></p>
        `;
    }

    // Reviews
    const reviewsList = document.getElementById('reviews-list');
    if (reviewsList) {
        if (place.reviews && place.reviews.length > 0) {
            reviewsList.innerHTML = '';
            place.reviews.forEach(review => {
                const card = document.createElement('div');
                card.className = 'review-card';
                card.innerHTML = `
                    <p class="rating">${'⭐'.repeat(review.rating)}</p>
                    <p class="author">By: ${review.user_name || 'Anonymous'}</p>
                    <p>${review.text}</p>
                `;
                reviewsList.appendChild(card);
            });
        } else {
            reviewsList.innerHTML = '<p>No reviews yet. Be the first!</p>';
        }
    }

    initMap(place.latitude, place.longitude, place.title);
    initLightbox(place.image_url);
}

/* === MAP === */

/**
 * Initialize Leaflet map centered on the place coordinates
 */
function initMap(latitude, longitude, title) {
    const map = L.map('map').setView([latitude, longitude], 13);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    L.marker([latitude, longitude])
        .addTo(map)
        .bindPopup(`<b>${title}</b>`)
        .openPopup();
}

/* === LIGHTBOX === */

/**
 * Initialize lightbox on hero image click
 */
function initLightbox(imageUrl) {
    if (!imageUrl) return;

    const hero = document.querySelector('.place-hero');
    const lightbox = document.getElementById('lightbox');
    const lightboxImg = document.getElementById('lightbox-img');
    const closeBtn = document.querySelector('.lightbox-close');

    if (!hero || !lightbox) return;

    lightboxImg.src = imageUrl;

    hero.addEventListener('click', () => {
        lightbox.classList.add('active');
    });

    closeBtn.addEventListener('click', () => {
        lightbox.classList.remove('active');
    });

    lightbox.addEventListener('click', (e) => {
        if (e.target === lightbox) {
            lightbox.classList.remove('active');
        }
    });

    // Close with Escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            lightbox.classList.remove('active');
        }
    });
}

/* === ADD REVIEW ACCESS === */
 
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
 * Show or hide add review section based on authentication
 * Attaches form submit handler to post review inline via API
 */
function checkAuthForReview(token, placeId) {
    const addReviewSection = document.getElementById('add-review');
 
    if (!addReviewSection) return;
 
    if (!token) {
        addReviewSection.style.display = 'none';
        return;
    }
 
    addReviewSection.style.display = 'block';
 
    const reviewForm = document.getElementById('review-form');
    if (!reviewForm) return;
 
    reviewForm.dataset.placeId = placeId;
 
    reviewForm.addEventListener('submit', async (event) => {
        event.preventDefault();
 
        const reviewText = document.getElementById('review-text').value.trim();
        const rating = document.getElementById('rating').value;
        const successMessage = document.getElementById('review-success');
        const errorMessage = document.getElementById('review-error');
 
        successMessage.textContent = '';
        errorMessage.textContent = '';
 
        if (!reviewText) {
            errorMessage.textContent = 'Please enter a review.';
            return;
        }
 
        try {
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
 
            if (response.ok) {
                successMessage.textContent = 'Review submitted successfully!';
                reviewForm.reset();
                // Refresh place details (reviews list) without full reload
                await fetchPlaceDetails(token, placeId);
            } else {
                const data = await response.json().catch(() => ({}));
                errorMessage.textContent = data.error || 'Failed to submit review. Please try again.';
            }
        } catch (err) {
            errorMessage.textContent = 'Connection error. Please try again.';
        }
    });
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
 