document.addEventListener('DOMContentLoaded', function() {
    const acc = document.getElementsByClassName("accordion");

    for (let i = 0; i < acc.length; i++) {
        acc[i].addEventListener("click", function() {
            /* Toggle between hiding and showing the active panel */
            let panel = this.nextElementSibling;

            if (panel.classList.contains('open')) {
                panel.classList.remove('open');
            } else {
                panel.classList.add('open');
            }
        });
    }

    // km slider
    const kmSlider = document.getElementById("km-slider");
    const kmValue = document.getElementById("km-value");

    kmSlider.addEventListener("input", function() {
        kmValue.textContent = this.value + " km";
    });
});