/* === ADD PLACE PAGE === */

const API_URL = 'http://localhost:5000/api/v1';

/**
 * Check authentication - redirect if not logged in
 */
function checkAuthentication() {
    const token = getCookie('token');
    if (!token) {
        window.location.href = 'login.html';
        return null;
    }
    return token;
}

/**
 * Get current user ID from JWT token
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
 * Load amenities from API and display as checkboxes
 */
async function loadAmenities(token) {
    try {
        const response = await fetch(`${API_URL}/amenities/`, {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            }
        });
        const amenities = await response.json();
        displayAmenities(amenities);
    } catch (err) {
        console.error('Failed to load amenities:', err);
    }
}

/**
 * Display amenities as checkboxes
 */
function displayAmenities(amenities) {
    const container = document.getElementById('amenities-list');
    if (!container) return;

    if (amenities.length === 0) {
        container.innerHTML = '<p>No amenities available.</p>';
        return;
    }

    container.innerHTML = amenities.map(amenity => `
        <label class="amenity-checkbox">
            <input type="checkbox" value="${amenity.id}" name="amenities">
            <span>${amenity.name}</span>
        </label>
    `).join('');
}

/**
 * Submit new place to API
 */
async function submitPlace(token, placeData) {
    const response = await fetch(`${API_URL}/places/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(placeData)
    });
    return response;
}

/**
 * Initialize add place page
 */
document.addEventListener('DOMContentLoaded', async () => {
    const token = checkAuthentication();
    if (!token) return;

    await loadAmenities(token);

    const form = document.getElementById('add-place-form');
    if (!form) return;

    form.addEventListener('submit', async (event) => {
        event.preventDefault();

        const successMessage = document.getElementById('success-message');
        const errorMessage = document.getElementById('error-message');
        successMessage.textContent = '';
        errorMessage.textContent = '';

        // Get selected amenities
        const selectedAmenities = Array.from(
            document.querySelectorAll('input[name="amenities"]:checked')
        ).map(cb => cb.value);

        const placeData = {
            title: document.getElementById('title').value.trim(),
            description: document.getElementById('description').value.trim(),
            price: parseFloat(document.getElementById('price').value),
            latitude: parseFloat(document.getElementById('latitude').value),
            longitude: parseFloat(document.getElementById('longitude').value),
            image_url: document.getElementById('image_url').value.trim() || null,
            owner_id: getUserIdFromToken(token),
            amenities: selectedAmenities
        };

        try {
            const response = await submitPlace(token, placeData);

            if (response.ok) {
                const data = await response.json();
                successMessage.textContent = 'Place created successfully!';
                setTimeout(() => {
                    window.location.href = `place.html?id=${data.id}`;
                }, 1500);
            } else {
                const data = await response.json().catch(() => ({}));
                errorMessage.textContent = data.message || data.error || 'Failed to create place.';
            }
        } catch (err) {
            errorMessage.textContent = 'Connection error. Please try again.';
        }
    });
});
