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
        const imageStyle = place.image_url
            ? `background-image: url('${place.image_url}'); background-size: cover; background-position: center;`
            : `background: linear-gradient(135deg, #e8e0d5, #d4c5b0);`;

        card.innerHTML = `
            <div class="card-image" style="${imageStyle}">
                <span class="card-badge">New</span>
                <span class="price-badge">$${place.price} / night</span>
                <button class="favorite-btn">❤️</button>
            </div>
            <div class="card-content">
                <h2>${place.title}</h2>
                <div class="card-meta">
                    <span class="card-reviews">⭐ ${place.reviews ? place.reviews.length : 0} reviews</span>
                </div>
                <p class="description">${place.description || ''}</p>
                <a href="place.html?id=${place.id}" class="details-button">View Details</a>
            </div>
        `;
        placesList.appendChild(card);
    });

    animateCards();
}

/* === FADE-IN OBSERVER === */

/**
 * Animate cards on scroll using IntersectionObserver
 */
function animateCards() {
    const cards = document.querySelectorAll('.place-card');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                setTimeout(() => {
                    entry.target.classList.add('visible');
                }, index * 100);
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });

    cards.forEach(card => observer.observe(card));
}

/* === PRICE FILTER === */

/**
 * Filter places by maximum price
 * @param {string} maxPrice - selected price value or 'all'
 */
function filterPlacesByPrice(maxPrice) {
    const cards = document.querySelectorAll('.place-card');

    cards.forEach(card => {
        const price = parseFloat(card.dataset.price);

        if (maxPrice === 'all') {
            card.style.display = 'block';
        } else {
            if (price <= parseFloat(maxPrice)) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        }
    });

    // Show message if no places match filter
    const placesList = document.getElementById('places-list');
    const visibleCards = document.querySelectorAll('.place-card[style="display: block;"]');
    const noResults = document.getElementById('no-results');

    if (visibleCards.length === 0) {
        if (!noResults) {
            const msg = document.createElement('p');
            msg.id = 'no-results';
            msg.textContent = 'No places match your filter.';
            placesList.appendChild(msg);
        }
    } else {
        if (noResults) noResults.remove();
    }
}
