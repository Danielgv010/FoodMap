document.addEventListener('DOMContentLoaded', function() {
    // Accordion functionality
    const accordions = document.querySelectorAll('.accordion');

    accordions.forEach(accordion => {
        accordion.addEventListener('click', function() {
            this.classList.toggle('active');
            const panel = this.nextElementSibling;
            if (panel.style.maxHeight) {
                panel.style.maxHeight = null;
            } else {
                panel.style.maxHeight = panel.scrollHeight + "px";
            }
        });
    });

    // KM Slider functionality
    const kmSlider = document.getElementById('km-slider');
    const kmValue = document.getElementById('km-value');

    if (kmSlider && kmValue) {
        kmSlider.addEventListener('input', function() {
            kmValue.textContent = this.value + " km";
        });
    }
});