// Kod do obsługi menu hamburgera
document.addEventListener('DOMContentLoaded', () => {
    const hamburgerBtn = document.getElementById('hamburger-btn');
    const mainNavLinks = document.getElementById('main-nav-links');

    if (hamburgerBtn && mainNavLinks) {
        hamburgerBtn.addEventListener('click', () => {
            mainNavLinks.classList.toggle('mobile-active');
        });
    }

    // Istniejący kod do stopki
    if (document.getElementById('current-year')) {
        document.getElementById('current-year').textContent = new Date().getFullYear();
    }
});