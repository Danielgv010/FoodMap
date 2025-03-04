document.addEventListener('DOMContentLoaded', function() {
    const acc = document.getElementsByClassName("accordion");

    for (let i = 0; i < acc.length; i++) {
        acc[i].addEventListener("click", function() {
            let panel = this.nextElementSibling;
            panel.style.setProperty('--panel-height', panel.scrollHeight + 'px');  /*Set the element panel of variable from panel style css*/
             panel.classList.toggle('open');    /*Set the class of variable set earlier to trigger the animations with animation value from .panel*/
        });
    }

    // km slider
    const kmSlider = document.getElementById("km-slider");
    const kmValue = document.getElementById("km-value");

    kmSlider.addEventListener("input", function() {
        kmValue.textContent = this.value + " km";
    });
});