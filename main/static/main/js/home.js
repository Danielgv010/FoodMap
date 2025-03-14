document.addEventListener('DOMContentLoaded', function() {
    // Accordion functionality
    const acc = document.getElementsByClassName("accordion");

    for (let i = 0; i < acc.length; i++) {
        acc[i].addEventListener("click", function() {
            let panel = this.nextElementSibling;
            const isOpen = panel.classList.contains('open');  // Check if panel is open

            if (!isOpen) {
                // Panel is being opened, so set the height
                panel.style.setProperty('--panel-height', panel.scrollHeight + 'px');
            } else {
                // Panel is being closed, set height to 0 to trigger animation
                panel.style.setProperty('--panel-height', '0px');
            }

            panel.classList.toggle('open'); // Toggle the 'open' class AFTER setting the height
        });
    }

    // km slider
    const kmSlider = document.getElementById("km-slider");
    const kmValue = document.getElementById("km-value");

    if (kmSlider && kmValue) {
        kmSlider.addEventListener("input", function() {
            kmValue.textContent = this.value + " km";
        });
    }

    // Review Form Functionality
    const addReviewButtons = document.querySelectorAll('.add-review-button');

    addReviewButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            const reviewFormContainer = this.closest('.panel-content-inner').querySelector('.review-form-container');
            const panel = this.closest('.panel'); // Get the accordion panel

            if (reviewFormContainer) {
                if (reviewFormContainer.style.display === 'block') {
                    // Form is already open, so close it
                    reviewFormContainer.style.display = 'none';
                     if (panel) {
                        panel.style.setProperty('--panel-height', panel.scrollHeight + 'px');
                    }

                } else {
                    // Form is closed, so open it and recalculate panel height
                    reviewFormContainer.style.display = 'block';
                    if (panel) {
                         panel.style.setProperty('--panel-height', panel.scrollHeight + 'px'); // Recalculate panel height
                         // Trigger a reflow to force the browser to recognize the new height.
                         panel.offsetHeight;
                         panel.style.setProperty('--panel-height', panel.scrollHeight + 'px');
                    }
                }
            }
        });
    });

    // Event listener for the cancel button
    document.querySelectorAll('.cancel-review-button').forEach(button => {
        button.addEventListener('click', function() {
            const reviewFormContainer = this.closest('.review-form-container');
            const panel = this.closest('.panel');  // Get the accordion panel

            if (reviewFormContainer) {
                reviewFormContainer.style.display = 'none';
                if (panel) {
                     panel.style.setProperty('--panel-height', panel.scrollHeight + 'px'); // Recalculate panel height
                }
            }
        });
    });


    // Form Submission
    const reviewForms = document.querySelectorAll('.review-form'); // Select by class
    reviewForms.forEach(form => {
        form.addEventListener('submit', function(event) {
            event.preventDefault();

            const restaurantId = form.dataset.restaurantId; // Use form to get the restaurantId
            const rating = form.querySelector('.rating').value; // Use form.querySelector
            const content = form.querySelector('.content').value; // Use form.querySelector
            const reviewMessage = form.closest('.review-form-container').querySelector('.review-message'); // Use class

            const formData = {
                restaurant: restaurantId,
                rating: rating,
                content: content
            };

            fetch(form.dataset.url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify(formData)
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                reviewMessage.textContent = 'Review submitted successfully!';
                reviewMessage.style.color = 'green';
                form.reset();
                form.closest('.review-form-container').style.display = 'none';
            })
            .catch(error => {
                console.error('Error:', error);
                reviewMessage.textContent = 'Error submitting review.';
                reviewMessage.style.color = 'red';
            });
        });
    });

    // CSRF token helper function (from Django documentation)
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Leaflet Map Integration
    const mapContainer = document.getElementById('map-container');

    if (mapContainer) {
        var map = L.map('map-container').setView([51.505, -0.09], 13); // Default London view

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(map);

        map.on('click', function(e) {
            const lat = e.latlng.lat;
            const lng = e.latlng.lng;
            console.log('Latitude: ' + lat + ', Longitude: ' + lng);
        });
    }

    // Search Functionality
    const searchInput = document.getElementById('search-input');
    const searchButton = document.getElementById('search-button');

    searchButton.addEventListener('click', function() {
        const searchTerm = searchInput.value;

        if (searchTerm) {
            fetch(`/search/api/search/?search=${encodeURIComponent(searchTerm)}`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! Status: ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
                    // Replace the contents of the menus container with the returned HTML
                    const menusContainer = document.querySelector('.menus-container');
                    menusContainer.innerHTML = data.menus_html;

                    // Re-initialize accordion functionality for the newly added menus.
                    initializeAccordions();
                 })
                .catch(error => {
                    console.error('Error:', error);
                });
        } else {
            alert('Please enter a search term.');
        }
    });

    function initializeAccordions() {
        const acc = document.getElementsByClassName("accordion");

        for (let i = 0; i < acc.length; i++) {
            acc[i].addEventListener("click", function() {
                let panel = this.nextElementSibling;
                const isOpen = panel.classList.contains('open');  // Check if panel is open

                if (!isOpen) {
                    // Panel is being opened, so set the height
                    panel.style.setProperty('--panel-height', panel.scrollHeight + 'px');
                } else {
                    // Panel is being closed, set height to 0 to trigger animation
                    panel.style.setProperty('--panel-height', '0px');
                }

                panel.classList.toggle('open'); // Toggle the 'open' class AFTER setting the height
            });
        }
    }
});