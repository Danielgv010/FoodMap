document.addEventListener('DOMContentLoaded', function() {
    const addMenuButton = document.getElementById('add-menu-button');

    if (addMenuButton) {
        addMenuButton.addEventListener('click', function() {
            window.location.href = addMenuButton.dataset.url;
        });
    }
});