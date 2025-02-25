document.addEventListener('DOMContentLoaded', function() {
    // Accordion functionality
    const deployTrigger = document.getElementById('deployTrigger');
    const locationGroup = document.getElementById('location-group');
    const triangle = document.querySelector('.triangle');
    const locationInput = locationGroup.querySelector('input'); // Get the input inside location-group

    deployTrigger.addEventListener('click', function() {
        locationGroup.classList.toggle('visible');
        triangle.classList.toggle('rotated');
    });

    // Check input on page load for label styling
    function checkInputValidity(inputElement) {
        if (inputElement.value) {
            inputElement.classList.add('valid');
        } else {
            inputElement.classList.remove('valid');
        }
    }

    // Apply initial check and listen for input events to update the label
    const inputs = document.querySelectorAll('.form-input-group input');
    inputs.forEach(input => {
        checkInputValidity(input); // Check on page load

        input.addEventListener('input', () => {
            checkInputValidity(input);
        });
    });

    //Fix for location input
    if (locationInput) {
        locationInput.addEventListener('input', function() {
            if (this.value) {
                this.setAttribute('valid', true);
            } else {
                this.removeAttribute('valid');
            }
        });

        // Initial check in case the input has a value on page load
        if (locationInput.value) {
            locationInput.setAttribute('valid', true);
        }
    }
});