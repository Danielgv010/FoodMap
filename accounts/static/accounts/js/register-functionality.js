document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form'); // Select the form element
    const submitButton = document.getElementById('submit'); //Select submit button

    submitButton.addEventListener('click', function(event) {
        event.preventDefault(); // Prevent the default form submission (page reload)

        const formData = new FormData(form); // Create a FormData object from the form

        if (!formData.has('location')) {
            formData.append('location', '');
        }

        fetch('/submit/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            console.log('Success:', data);
            alert('Registration successful!');
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Registration failed: ' + error);
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