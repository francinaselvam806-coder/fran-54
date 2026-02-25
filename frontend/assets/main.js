const API_URL = "http://127.0.0.1:8000";

async function postData(url, data) {
    const response = await fetch(`${API_URL}${url}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });
    return response.json();
}

async function getData(url) {
    const response = await fetch(`${API_URL}${url}`);
    return response.json();
}

function getLocation() {
    return new Promise((resolve, reject) => {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    resolve({
                        lat: position.coords.latitude,
                        lon: position.coords.longitude
                    });
                },
                (error) => {
                    reject(error);
                }
            );
        } else {
            reject(new Error("Geolocation is not supported by this browser."));
        }
    });
}

function updateHeader() {
    const user = JSON.parse(localStorage.getItem('user'));
    const authLinks = document.getElementById('auth-links');
    const userProfile = document.getElementById('user-profile');
    const userName = document.getElementById('user-name');
    const userImgContainer = document.getElementById('user-img-container');

    if (user && authLinks && userProfile) {
        authLinks.classList.add('hidden');
        userProfile.classList.remove('hidden');
        if (userName) userName.innerText = user.username;
        if (userImgContainer) {
            userImgContainer.innerHTML = user.profile_image
                ? `<img src="${user.profile_image}" class="w-full h-full object-cover rounded-full">`
                : `<span class="material-symbols-outlined">person</span>`;
        }
    }
}


function updateLandingPage() {
    const user = JSON.parse(localStorage.getItem('user'));
    const primaryBtn = document.getElementById('hero-primary-btn');
    const secondaryBtn = document.getElementById('hero-secondary-btn');

    // Only run this logic if we are on the landing page (buttons exist)
    if (primaryBtn) {
        if (!user) {
            // Not logged in: Default View
            primaryBtn.href = "register.html?role=client";
            primaryBtn.innerHTML = `
                <span class="mr-2 material-symbols-outlined text-[20px]">search</span>
                <span>Find a Helper</span>
            `;

            if (secondaryBtn) {
                secondaryBtn.href = "register.html?role=student";
                secondaryBtn.style.display = 'flex'; // Ensure visible
                secondaryBtn.innerHTML = `
                    <span class="mr-2 material-symbols-outlined text-[20px] text-primary">work</span>
                    <span>Earn Money</span>
                `;
            }
        } else {
            // Logged In
            if (user.is_provider) {
                // Student Role
                primaryBtn.href = "post.html";
                primaryBtn.innerHTML = `
                    <span class="mr-2 material-symbols-outlined text-[20px]">add_task</span>
                    <span>Post a Service</span>
                `;

                // Hide or repurpose secondary button for students
                if (secondaryBtn) {
                    secondaryBtn.style.display = 'none'; // Or change to "My Services"
                }

            } else {
                // Client / Hirer Role
                primaryBtn.href = "services.html"; // AI Assistant / Find Services
                primaryBtn.innerHTML = `
                    <span class="mr-2 material-symbols-outlined text-[20px]">smart_toy</span>
                    <span>AI Assistant</span>
                `;

                // Hide secondary button for clients (or maybe keep it as "Become a Provider"?)
                // For now, hiding to keep flow focused as per request
                if (secondaryBtn) {
                    secondaryBtn.style.display = 'none';
                }
            }
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    updateHeader();
    updateLandingPage();
});
