document.addEventListener('DOMContentLoaded', function() {
    // Deploy Trigger Logic
    const deployTrigger = document.getElementById('deployTrigger');
    const locationInputs = document.getElementById('location-inputs');
    const triangle = document.querySelector('.triangle');

    if (deployTrigger) {
        deployTrigger.addEventListener('click', function() {
            locationInputs.classList.toggle('visible');
            triangle.classList.toggle('rotated');
        });
    }

    // Input Validation Logic
    function checkInputValidity(inputElement) {
        if (inputElement.value) {
            inputElement.classList.add('valid');
        } else {
            inputElement.classList.remove('valid');
        }
    }

    const inputs = document.querySelectorAll('.form-input-group input');
    inputs.forEach(input => {
        checkInputValidity(input);

        input.addEventListener('input', () => {
            checkInputValidity(input);
        });
    });

    // Registration Form Submission
    const registrationForm = document.getElementById('registrationForm');
    if (registrationForm) {
        const apiUrl = registrationForm.dataset.url;

        registrationForm.addEventListener('submit', function(event) {
            event.preventDefault();

            const formData = new FormData(registrationForm);
            const street = document.getElementById('street').value;
            const zip = document.getElementById('zip').value;
            const country = document.getElementById('country').value;
            const location = `${street},${zip},${country}`;

            if ((street && !zip && !country)|| (!street && zip && !country) || (!street && !zip && country)) {
                alert('Please fill in the location fields.');
                return;
            }

            formData.append('location', location);

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
                window.location.href = "/"; // Redirect after registration
            })
            .catch(error => {
                console.error('Registration error:', error);

                if (error && typeof error === 'object') {
                    if(error.detail){
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
});