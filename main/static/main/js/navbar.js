document.addEventListener("DOMContentLoaded", function() {
    const hamburger = document.querySelector(".hamburger");
    const navMenu = document.querySelector(".nav-menu");
    const loginButton = document.querySelector(".login");
    const loginModal = document.querySelector(".login-modal");
    const closeButton = document.querySelector(".close-button");
    const modalOverlay = document.getElementById("modal-overlay");

    hamburger.addEventListener("click", () => {
        hamburger.classList.toggle("is-active");

        const isActive = navMenu.classList.contains("active");

        if (!isActive) {
            navMenu.classList.add("active");
            navMenu.offsetHeight;
            requestAnimationFrame(() => {
                navMenu.style.maxHeight = navMenu.scrollHeight + "px";
            });
        } else {
            navMenu.style.maxHeight = "0";
            navMenu.addEventListener("transitionend", function() {
                navMenu.classList.remove("active");
                navMenu.removeEventListener("transitionend", arguments.callee);
            });
        }
    });

    loginButton.addEventListener("click", () => {
        loginModal.classList.add("active");
        modalOverlay.classList.add("active");
    });

    closeButton.addEventListener("click", () => {
        loginModal.classList.remove("active");
        modalOverlay.classList.remove("active");
    });

    modalOverlay.addEventListener("click", () => {
        loginModal.classList.remove("active");
        modalOverlay.classList.remove("active");
    });
});