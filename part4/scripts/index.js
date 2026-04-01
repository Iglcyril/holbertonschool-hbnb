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

/* === FETCH PLACES === */

/**
 * Fetch all places from API
 */
async function fetchPlaces(token) {
    try {
        const headers = { 'Content-Type': 'application/json' };
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const response = await fetch(`${API_URL}/places/`, { headers });

        if (!response.ok) {
            throw new Error('Failed to fetch places');
        }

        const places = await response.json();
        allPlaces = places;
        displayPlaces(places);
    } catch (err) {
        const placesList = document.getElementById('places-list');
        if (placesList) {
            placesList.innerHTML = '<p class="error-message">Failed to load places. Please try again.</p>';
        }
    }
}

/**
 * Display places as cards in the places list
 */
function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    if (!placesList) return;

    placesList.innerHTML = '';

    if (places.length === 0) {
        placesList.innerHTML = '<p>No places found.</p>';
        return;
    }

    places.forEach(place => {
        const card = document.createElement('div');
        card.className = 'place-card';
        card.dataset.price = place.price;
        card.innerHTML = `
            <h2>${place.title}</h2>
            <p class="price">$${place.price} / night</p>
            <p>${place.description || ''}</p>
            <a href="place.html?id=${place.id}" class="details-button">View Details</a>
        `;
        placesList.appendChild(card);
    });
}
