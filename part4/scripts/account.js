/* === ACCOUNT PAGE === */

const API_URL = 'http://localhost:5000/api/v1';

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
 * Get user initials for avatar
 */
function getInitials(firstName, lastName) {
    return `${firstName.charAt(0)}${lastName.charAt(0)}`.toUpperCase();
}

/**
 * Fetch user info and populate the page
 */
async function loadUserInfo(token, userId) {
    try {
        const response = await fetch(`${API_URL}/users/${userId}`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (!response.ok) throw new Error('Failed to fetch user');

        const user = await response.json();

        document.getElementById('account-fullname').textContent = `${user.first_name} ${user.last_name}`;
        document.getElementById('account-email').textContent = user.email;
        document.getElementById('info-firstname').textContent = user.first_name;
        document.getElementById('info-lastname').textContent = user.last_name;
        document.getElementById('info-email').textContent = user.email;

        // Avatar: photo or initials
        const avatarImg = document.getElementById('account-avatar-img');
        const avatarInitials = document.getElementById('account-avatar-initials');
        if (user.profile_picture_url) {
            avatarImg.src = user.profile_picture_url;
            avatarImg.style.display = 'block';
            avatarInitials.style.display = 'none';
        } else {
            avatarInitials.textContent = getInitials(user.first_name, user.last_name);
        }

        // Pre-fill profile form
        document.getElementById('profile-picture').value = user.profile_picture_url || '';
        document.getElementById('bio').value = user.bio || '';
    } catch (err) {
        document.getElementById('account-fullname').textContent = 'Error loading profile';
    }
}

/**
 * Save bio and profile picture
 */
async function initProfileForm(token, userId) {
    const form = document.getElementById('profile-form');
    if (!form) return;

    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        const successMsg = document.getElementById('profile-success');
        const errorMsg = document.getElementById('profile-error');
        successMsg.textContent = '';
        errorMsg.textContent = '';

        const payload = {
            bio: document.getElementById('bio').value.trim() || null,
            profile_picture_url: document.getElementById('profile-picture').value.trim() || null
        };

        try {
            const response = await fetch(`${API_URL}/users/${userId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(payload)
            });

            if (response.ok) {
                const user = await response.json();
                successMsg.textContent = 'Profile updated successfully!';

                // Update avatar live
                const avatarImg = document.getElementById('account-avatar-img');
                const avatarInitials = document.getElementById('account-avatar-initials');
                if (user.profile_picture_url) {
                    avatarImg.src = user.profile_picture_url;
                    avatarImg.style.display = 'block';
                    avatarInitials.style.display = 'none';
                } else {
                    avatarImg.style.display = 'none';
                    avatarInitials.style.display = 'inline';
                }
            } else {
                const data = await response.json().catch(() => ({}));
                errorMsg.textContent = data.error || 'Failed to update profile.';
            }
        } catch (err) {
            errorMsg.textContent = 'Connection error. Please try again.';
        }
    });
}

/**
 * Fetch all places and display those owned by the current user
 */
async function loadUserPlaces(token, userId) {
    try {
        const response = await fetch(`${API_URL}/places/`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });

        const places = await response.json();
        const myPlaces = places.filter(p => p.owner_id === userId);

        document.getElementById('stat-places').textContent = myPlaces.length;

        const container = document.getElementById('account-places');

        if (myPlaces.length === 0) {
            container.innerHTML = '<p class="no-top-rated">You have not listed any places yet. <a href="add_place.html">Add one!</a></p>';
            return;
        }

        container.innerHTML = myPlaces.map(place => {
            const imageStyle = place.image_url
                ? `background-image: url('${place.image_url}'); background-size: cover; background-position: center;`
                : `background: linear-gradient(135deg, #e8e0d5, #d4c5b0);`;
            return `
                <div class="account-place-card" id="place-card-${place.id}">
                    <div class="account-place-image" style="${imageStyle}"></div>
                    <div class="account-place-content">
                        <h3>${place.title}</h3>
                        <p class="account-place-price">$${place.price} / night</p>
                        <div class="account-place-actions">
                            <a href="place.html?id=${place.id}" class="details-button">View</a>
                            <button class="delete-place-btn" data-id="${place.id}">Delete</button>
                        </div>
                    </div>
                </div>
            `;
        }).join('');

        // Attach delete listeners
        container.querySelectorAll('.delete-place-btn').forEach(btn => {
            btn.addEventListener('click', async () => {
                const placeId = btn.dataset.id;
                if (!confirm('Delete this place? This action cannot be undone.')) return;

                const res = await fetch(`${API_URL}/places/${placeId}`, {
                    method: 'DELETE',
                    headers: { 'Authorization': `Bearer ${token}` }
                });

                if (res.ok) {
                    document.getElementById(`place-card-${placeId}`).remove();
                    const count = parseInt(document.getElementById('stat-places').textContent) - 1;
                    document.getElementById('stat-places').textContent = count;
                } else {
                    alert('Failed to delete place.');
                }
            });
        });
    } catch (err) {
        document.getElementById('account-places').innerHTML = '<p class="error-message">Failed to load places.</p>';
    }
}

/**
 * Fetch reviews written by the user (count only)
 */
async function loadUserReviewsCount(token, userId) {
    try {
        const response = await fetch(`${API_URL}/reviews/`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        const reviews = await response.json();
        const myReviews = reviews.filter(r => r.user_id === userId);
        document.getElementById('stat-reviews').textContent = myReviews.length;
    } catch (err) {
        document.getElementById('stat-reviews').textContent = '—';
    }
}

/**
 * Initialize account page
 */
document.addEventListener('DOMContentLoaded', async () => {
    const token = getCookie('token');
    if (!token) {
        window.location.href = 'login.html';
        return;
    }

    const userId = getUserIdFromToken(token);
    if (!userId) {
        window.location.href = 'login.html';
        return;
    }

    await loadUserInfo(token, userId);
    await loadUserPlaces(token, userId);
    loadUserReviewsCount(token, userId);
    initProfileForm(token, userId);
});
