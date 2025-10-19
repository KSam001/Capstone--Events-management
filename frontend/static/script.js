const API_URL = 'http://127.0.0.1:8000/api/';

// DOM Elements
const authBtn = document.getElementById('auth-btn');
const logoutBtn = document.getElementById('logout-btn');
const createEventBtn = document.getElementById('create-event-btn');
const authFormDiv = document.getElementById('auth-form');
const eventFormDiv = document.getElementById('event-form');
const eventsList = document.getElementById('events-list');
const loginForm = document.getElementById('login-form');
const registerForm = document.getElementById('register-form');
const newEventForm = document.getElementById('new-event-form');
const closeBtns = document.querySelectorAll('.close-btn');

let accessToken = localStorage.getItem('access');
let refreshToken = localStorage.getItem('refresh');

// --- UTILITY FUNCTIONS ---

function updateAuthUI() {
    const isAuthenticated = !!accessToken;
    authBtn.style.display = isAuthenticated ? 'none' : 'block';
    logoutBtn.style.display = isAuthenticated ? 'block' : 'none';
    createEventBtn.style.display = isAuthenticated ? 'block' : 'none';
    authFormDiv.style.display = 'none';
    eventFormDiv.style.display = 'none';
}

function fetchWrapper(url, options = {}) {
    if (accessToken) {
        options.headers = {
            ...options.headers,
            'Authorization': `Bearer ${accessToken}`,
        };
    }
    
    // Default headers
    options.headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };

    return fetch(url, options)
        .then(response => {
            if (!response.ok) {
                // If a 401 Unauthorized occurs, try refreshing the token
                if (response.status === 401 && refreshToken) {
                    return refreshAndRetry(url, options);
                }
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            // Handle 204 No Content for delete/cancel actions
            if (response.status === 204) return null;
            return response.json();
        });
}

function refreshAndRetry(url, originalOptions) {
    console.log("Token expired. Attempting refresh...");
    return fetch(`${API_URL}token/refresh/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh: refreshToken })
    })
    .then(res => res.json())
    .then(data => {
        if (data.access) {
            accessToken = data.access;
            localStorage.setItem('access', accessToken);
            
            // Update authorization header for original request and retry
            originalOptions.headers['Authorization'] = `Bearer ${accessToken}`;
            return fetch(url, originalOptions)
                .then(response => response.json());
        } else {
            throw new Error("Token refresh failed. Please log in.");
        }
    })
    .catch(() => {
        logout();
        throw new Error("Session expired. Please log in again.");
    });
}

// --- AUTH LOGIC ---

function logout() {
    accessToken = null;
    refreshToken = null;
    localStorage.removeItem('access');
    localStorage.removeItem('refresh');
    alert('Logged out.');
    updateAuthUI();
    loadEvents(); // Reload events to show only read-only view
}

loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;

    try {
        const data = await fetchWrapper(`${API_URL}token/`, {
            method: 'POST',
            body: JSON.stringify({ email, password }),
            headers: { 'Content-Type': 'application/json', 'Authorization': null } // Override Auth header for login
        });

        accessToken = data.access;
        refreshToken = data.refresh;
        localStorage.setItem('access', accessToken);
        localStorage.setItem('refresh', refreshToken);
        
        alert('Login successful!');
        updateAuthUI();
        loadEvents();
    } catch (error) {
        console.error('Login error:', error);
        alert('Login failed. Check your credentials.');
    }
});

registerForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const payload = {
        first_name: document.getElementById('reg-fname').value,
        last_name: document.getElementById('reg-lname').value,
        email: document.getElementById('reg-email').value,
        date_of_birth: document.getElementById('reg-dob').value,
        password: document.getElementById('reg-password').value,
    };

    try {
        await fetchWrapper(`${API_URL}register/`, {
            method: 'POST',
            body: JSON.stringify(payload),
            headers: { 'Content-Type': 'application/json', 'Authorization': null }
        });

        alert('Registration successful! Please log in.');
        registerForm.reset();
        // Show login form after registration
        document.getElementById('auth-form').style.display = 'block';
    } catch (error) {
        console.error('Registration error:', error);
        alert('Registration failed. Email might be in use or password too weak.');
    }
});

// --- EVENT LOGIC ---

async function loadEvents() {
    eventsList.innerHTML = '<p>Loading events...</p>';
    try {
        const events = await fetchWrapper(`${API_URL}events/`);
        eventsList.innerHTML = '';
        
        events.forEach(event => {
            const isHost = event.host === getCurrentUserId(); // Simple host check
            const eventItem = document.createElement('div');
            eventItem.className = 'card event-item';
            eventItem.innerHTML = `
                <div class="event-details">
                    <h3>${event.title} (${event.date} at ${event.time})</h3>
                    <p>${event.description}</p>
                    <p class="event-host">Location: ${event.location} | Hosted by: ${event.host_email}</p>
                </div>
                <div class="event-actions">
                    <button class="rsvp-btn" data-event-id="${event.id}">RSVP / Cancel</button>
                    ${isHost ? `<button class="delete-btn" data-event-id="${event.id}">Delete</button>` : ''}
                </div>
            `;
            eventsList.appendChild(eventItem);
        });

        document.querySelectorAll('.rsvp-btn').forEach(button => {
            button.addEventListener('click', handleRsvp);
        });
        document.querySelectorAll('.delete-btn').forEach(button => {
            button.addEventListener('click', handleDelete);
        });

    } catch (error) {
        console.error('Failed to load events:', error);
        eventsList.innerHTML = `<p>Error loading events: ${error.message}. Please check API server status.</p>`;
    }
}

newEventForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const payload = {
        title: document.getElementById('event-title').value,
        description: document.getElementById('event-description').value,
        date: document.getElementById('event-date').value,
        time: document.getElementById('event-time').value,
        location: document.getElementById('event-location').value,
    };

    try {
        await fetchWrapper(`${API_URL}events/`, {
            method: 'POST',
            body: JSON.stringify(payload)
        });
        alert('Event created successfully!');
        newEventForm.reset();
        eventFormDiv.style.display = 'none';
        loadEvents();
    } catch (error) {
        console.error('Create event error:', error);
        alert(`Failed to create event. Error: ${error.message}`);
    }
});

async function handleRsvp(e) {
    const eventId = e.target.dataset.eventId;
    if (!accessToken) {
        alert("You must be logged in to RSVP.");
        return;
    }

    try {
        const result = await fetchWrapper(`${API_URL}events/${eventId}/rsvp/`, {
            method: 'POST'
        });
        
        if (result && result.status === 'RSVP successful') {
            alert('RSVP successful!');
        } else if (result === null) {
            alert('RSVP cancelled.');
        } else {
            alert('Action failed.');
        }
        loadEvents();
    } catch (error) {
        console.error('RSVP error:', error);
        alert(`RSVP failed. Error: ${error.message}`);
    }
}

async function handleDelete(e) {
    const eventId = e.target.dataset.eventId;
    if (!confirm('Are you sure you want to delete this event? This action cannot be undone.')) return;

    try {
        // DELETE request (returns 204 No Content, thus fetchWrapper returns null)
        await fetchWrapper(`${API_URL}events/${eventId}/`, {
            method: 'DELETE'
        });
        
        alert('Event deleted successfully!');
        loadEvents();
    } catch (error) {
        console.error('Delete error:', error);
        alert(`Failed to delete event. Error: ${error.message}`);
    }
}

function getCurrentUserId() {
    // Decode JWT to get user ID (simplistic and non-secure way for a simple frontend)
    if (!accessToken) return null;
    try {
        const payload = JSON.parse(atob(accessToken.split('.')[1]));
        return payload.user_id;
    } catch (e) {
        return null;
    }
}


// --- EVENT LISTENERS ---
authBtn.addEventListener('click', () => authFormDiv.style.display = 'block');
logoutBtn.addEventListener('click', logout);
createEventBtn.addEventListener('click', () => eventFormDiv.style.display = 'block');
closeBtns.forEach(btn => btn.addEventListener('click', (e) => {
    e.target.closest('.card').style.display = 'none';
}));


// --- INITIALIZATION ---
updateAuthUI();
loadEvents();
