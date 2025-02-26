document.addEventListener('DOMContentLoaded', function() {
    const deployTrigger = document.getElementById('deployTrigger');
    const locationInputs = document.getElementById('location-inputs');
    const triangle = document.querySelector('.triangle');

    deployTrigger.addEventListener('click', function() {
        locationInputs.classList.toggle('visible');
        triangle.classList.toggle('rotated');
    });

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

    const form = document.getElementById('registrationForm');
    const apiUrl = form.dataset.url;

    form.addEventListener('submit', function(event) {
        event.preventDefault();

        const formData = new FormData(form);
        const street = document.getElementById('street').value;
        const zip = document.getElementById('zip').value;
        const country = document.getElementById('country').value;
        const location = `${street},${zip},${country}`;

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
            window.location.href = "/"

        })
        .catch(error => {
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