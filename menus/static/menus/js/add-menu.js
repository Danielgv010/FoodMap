document.addEventListener('DOMContentLoaded', function() {
    const addMenuForm = document.getElementById('add-menu-form');
    const addDishButton = document.getElementById('add-dish-button');
    const dishesContainer = document.getElementById('dishes-container');
    let dishCount = 1; // Start from 1 since there's already one dish row.
    const autocompleteButton = document.getElementById('autocomplete-button');
    const ocrApiUrl = addMenuForm.dataset.ocrUrl;  // Retrieve the OCR API URL
    const apiUrl = addMenuForm.dataset.url;

    // Function to add a new dish row
    function addDishRow() {
        const newDishRow = document.createElement('div');
        newDishRow.classList.add('dish-row');
        newDishRow.innerHTML = `
            <div class="form-group">
                <label for="dish_name_${dishCount}">Dish Name:</label>
                <input type="text" id="dish_name_${dishCount}" name="dish_name[]">
            </div>
            <div class="form-group">
                <label for="dish_price_${dishCount}">Dish Price:</label>
                <input type="number" id="dish_price_${dishCount}" name="dish_price[]" step="0.01">
            </div>
            <div class="form-group">
                <label for="dish_promoted_${dishCount}">Promoted:</label>
                <input type="checkbox" id="dish_promoted_${dishCount}" name="dish_promoted[]">
            </div>
            <button type="button" class="delete-dish-button">Delete</button>
        `;

        dishesContainer.appendChild(newDishRow);

        // Add event listener to the delete button for the new row
        const deleteButton = newDishRow.querySelector('.delete-dish-button');
        deleteButton.addEventListener('click', function() {
            newDishRow.remove();
        });

        dishCount++;
    }

    // Event listener for adding a new dish row
    if (addDishButton) {
        addDishButton.addEventListener('click', addDishRow);
    }

    // Event delegation for deleting dish rows
    dishesContainer.addEventListener('click', function(event) {
        if (event.target.classList.contains('delete-dish-button')) {
            event.target.closest('.dish-row').remove();
        }
    });

    // OCR and Form Population Function
    function populateFormFromOcr(extractedJson) {
        if (extractedJson.is_more_than_one_menu === true) {
            alert('The uploaded document seems to contain multiple menus. Please upload a document with only one menu.');
            return; // Stop form population
        }

        const menuPriceElement = document.getElementById('menu_price');
        const setMenuElement = document.getElementById('set_menu');

        if (extractedJson.price !== undefined) {
            menuPriceElement.value = extractedJson.price;
        }

        if (extractedJson.is_more_than_one_menu !== undefined) {
            setMenuElement.checked = extractedJson.is_more_than_one_menu;
        }


        // Clear existing dish rows (except the first one)
        while (dishesContainer.children.length > 1) {
            dishesContainer.removeChild(dishesContainer.lastChild);
        }

        // Repopulate dish rows
        if (extractedJson.products && Array.isArray(extractedJson.products)) {
            extractedJson.products.forEach((product, index) => {
                if (index > 0) {
                    addDishRow(); // Add a new row for each product after the first
                }
                const dishNameInput = document.querySelector(`#dish_name_${index}`); //Select the first row always
                if (dishNameInput) {
                    dishNameInput.value = product;
                }
            });
        }
    }

   // Autocomplete button click handler
    if (autocompleteButton) {
        autocompleteButton.addEventListener('click', function(event) {
            event.preventDefault();

            // Create an invisible file input element
            const fileInput = document.createElement('input');
            fileInput.type = 'file';
            fileInput.accept = '.pdf';
            fileInput.style.display = 'none'; // Hide the input

            // Listen for the file selection
            fileInput.addEventListener('change', function(event) {
                const pdfFile = event.target.files[0];

                if (!pdfFile) {
                    alert('Please select a PDF file.');
                    return;
                }

                const formData = new FormData();
                formData.append('pdf_file', pdfFile);

                fetch(ocrApiUrl, {
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
                    console.log('OCR Data:', data);

                    if (data.extracted_json) {
                        populateFormFromOcr(data.extracted_json);
                    } else {
                        alert('No extracted data found.');
                    }
                })
                .catch(error => {
                    console.error('Error during OCR:', error);
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

                // Remove the file input after processing
                document.body.removeChild(fileInput);
            });

            // Add the file input to the document and trigger the click event
            document.body.appendChild(fileInput);
            fileInput.click();
        });
    }


    // Form submission handling
    if (addMenuForm) {
        addMenuForm.addEventListener('submit', function(event) {
            event.preventDefault(); // Prevent the default form submission


            // Get form data
            const menuNameElement = document.getElementById('menu_name');
            const menuName = menuNameElement ? menuNameElement.value : '';

            const menuPriceElement = document.getElementById('menu_price');
            const menuPrice = menuPriceElement ? menuPriceElement.value : '';

            const setMenuElement = document.getElementById('set_menu');
            const setMenu = setMenuElement ? setMenuElement.checked : false;


            const dishNames = Array.from(document.querySelectorAll('input[name="dish_name[]"]')).map(input => input.value);
            const dishPrices = Array.from(document.querySelectorAll('input[name="dish_price[]"]')).map(input => input.value);
            const dishPromoted = Array.from(document.querySelectorAll('input[name="dish_promoted[]"]')).map(checkbox => checkbox.checked);

            // Create data object
            const data = {
                menu_name: menuName,
                menu_price: menuPrice,
                set_menu: setMenu,
                dish_name: dishNames,
                dish_price: dishPrices,
                dish_promoted: dishPromoted
            };

            console.log('Form Data:', data);

            fetch(apiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify(data)
            })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(err => { throw err; });
                }
                return response.json();
            })
            .then(data => {
                alert('Menu saved successfully!');
                // Optionally redirect or clear the form
                window.location.href = "/";
            })
            .catch(error => {
                console.error('Error saving menu:', error);
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