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

    const form = document.getElementById('add-place-form');
    if (!form) return;

    // Attach submit listener immediately, before awaiting amenities
    form.addEventListener('submit', async (event) => {
        event.preventDefault();

        const currentToken = getCookie('token');
        const successMessage = document.getElementById('success-message');
        const errorMessage = document.getElementById('error-message');
        successMessage.textContent = '';
        errorMessage.textContent = '';

        const title = document.getElementById('title').value.trim();
        const description = document.getElementById('description').value.trim();
        const price = document.getElementById('price').value;
        const latitude = document.getElementById('latitude').value;
        const longitude = document.getElementById('longitude').value;

        if (!title || !description || !price || !latitude || !longitude) {
            errorMessage.textContent = 'Please fill all required fields.';
            return;
        }

        const selectedAmenities = Array.from(
            document.querySelectorAll('input[name="amenities"]:checked')
        ).map(cb => cb.value);

        const placeData = {
            title,
            description,
            price: parseFloat(price),
            latitude: parseFloat(latitude),
            longitude: parseFloat(longitude),
            image_url: document.getElementById('image_url').value.trim() || null,
            owner_id: getUserIdFromToken(currentToken),
            amenities: selectedAmenities
        };

        try {
            const response = await submitPlace(currentToken, placeData);

            if (response.ok) {
                const data = await response.json().catch(() => ({}));

                // Send additional images
                const imageUrls = [
                    document.getElementById('image_url_2').value.trim(),
                    document.getElementById('image_url_3').value.trim(),
                    document.getElementById('image_url_4').value.trim()
                ].filter(url => url !== '');

                for (const url of imageUrls) {
                    await fetch(`${API_URL}/places/${data.id}/images`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': `Bearer ${currentToken}`
                        },
                        body: JSON.stringify({ image_url: url, is_primary: false })
                    });
                }

                successMessage.textContent = 'Place created successfully!';
                window.location.replace('http://localhost:5500/part4/index.html');
            } else {
                const data = await response.json().catch(() => ({}));
                errorMessage.textContent = data.message || data.error || 'Failed to create place.';
            }
        } catch (err) {
            errorMessage.textContent = 'Connection error. Please try again.';
        }
    });

    // Load amenities after listener is attached
    await loadAmenities(token);
});
 