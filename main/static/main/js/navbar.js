document.addEventListener("DOMContentLoaded", function() {
    const hamburger = document.querySelector(".hamburger");
    const navMenu = document.querySelector(".nav-menu");
    const loginButton = document.querySelector(".login");
    const loginModal = document.querySelector(".login-modal");
    const closeButton = document.querySelector(".close-button");
    const modalOverlay = document.getElementById("modal-overlay");

    hamburger.addEventListener("click", () => {
        hamburger.classList.toggle("is-active");

        const isActive = navMenu.classList.contains("active");

        if (!isActive) {
            navMenu.classList.add("active");
            navMenu.offsetHeight;
            requestAnimationFrame(() => {
                navMenu.style.maxHeight = navMenu.scrollHeight + "px";
            });
        } else {
            navMenu.style.maxHeight = "0";
            navMenu.addEventListener("transitionend", function() {
                navMenu.classList.remove("active");
                navMenu.removeEventListener("transitionend", arguments.callee);
            });
        }
    });

    if(loginButton){
        loginButton.addEventListener("click", () => {
            loginModal.classList.add("active");
            modalOverlay.classList.add("active");
        });
    }

    if(closeButton){
        closeButton.addEventListener("click", () => {
            loginModal.classList.remove("active");
            modalOverlay.classList.remove("active");
        });
    }

    if(modalOverlay){
        modalOverlay.addEventListener("click", () => {
            loginModal.classList.remove("active");
            modalOverlay.classList.remove("active");
        });
    }

    // Login Form Submission
    const loginForm = document.getElementById('loginForm');

    if (loginForm) {
        loginForm.addEventListener('submit', function(event) {
            event.preventDefault();

            const apiUrl = loginForm.dataset.url;

            const formData = new FormData(loginForm);

            fetch(apiUrl, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                }
            })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(err => { throw err; });
                }
                return response.json();
            })
            .then(data => {
                window.location.href = "/";
            })
            .catch(error => {
                console.error('Login error:', error);

                if (error && typeof error === 'object') {
                    if(error.error){
                      alert(error.error); // Display the error message from the API
                    }
                    else if(error.detail){
                        alert(JSON.stringify(error.detail));
                      } else {
                        alert(JSON.stringify(error));
                      }

                } else {
                    alert('An error occurred: ' + error);
                }
            });
        });
    }

    // Logout Logic
    const logoutButton = document.getElementById('logoutButton');
    if (logoutButton) {

        const apiUrl = logoutButton.dataset.url;

        logoutButton.addEventListener('click', function() {
            fetch(apiUrl, {  // Replace '/logout/' with your logout URL
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                }
            })
            .then(response => {
                if (response.ok) {
                    window.location.href = "/";  // Reload the page to reflect logout
                } else {
                    console.error('Logout failed');
                    alert('Logout failed.');
                }
            })
            .catch(error => {
                console.error('Logout error:', error);
                alert('An error occurred during logout.');
            });
        });
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Add Menu Logic

    const manageMenusButton = document.getElementById('manageMenusButton');

    if(manageMenusButton){
        manageMenusButton.addEventListener("click", function() {
            window.location.href = manageMenusButton.dataset.url;
        });
    }

});