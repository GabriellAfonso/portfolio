// Apply saved theme before paint to avoid flash
(function () {
    if (localStorage.getItem('theme') === 'light') {
        document.body.classList.add('light-theme');
    }
})();

document.addEventListener('DOMContentLoaded', function () {
    const themeBtn = document.getElementById('theme-toggle');

    const iconSun = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>';
    const iconMoon = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>';

    function updateThemeIcon() {
        themeBtn.innerHTML = document.body.classList.contains('light-theme') ? iconSun : iconMoon;
    }

    updateThemeIcon();

    themeBtn.addEventListener('click', function () {
        document.body.classList.toggle('light-theme');
        localStorage.setItem('theme', document.body.classList.contains('light-theme') ? 'light' : 'dark');
        updateThemeIcon();
    });


    const toggleBtn = document.getElementById('menu');
    const navegationBar = document.getElementById('bar');
    const menuItems = document.querySelectorAll('#bar a');

    if (toggleBtn && navegationBar) {
        toggleBtn.addEventListener('click', function (event) {
            event.stopPropagation();
            navegationBar.classList.toggle('active');
            toggleBtn.classList.toggle('active');
        });

        document.addEventListener('click', function (event) {
            if (!navegationBar.contains(event.target) && event.target !== toggleBtn && !toggleBtn.contains(event.target)) {
                navegationBar.classList.remove('active');
                toggleBtn.classList.remove('active');
            }
        });

        menuItems.forEach(function (menuItem) {
            menuItem.addEventListener('click', function () {
                navegationBar.classList.remove('active');
                toggleBtn.classList.remove('active');
            });
        });

        const closeBtn = document.getElementById('close-menu');
        if (closeBtn) {
            closeBtn.addEventListener('click', function () {
                navegationBar.classList.remove('active');
                toggleBtn.classList.remove('active');
            });
        }
    }

    const reveals = document.querySelectorAll('.reveal');

    function checkReveal() {
        const windowHeight = window.innerHeight;
        const revealPoint = 100;
        reveals.forEach(function (reveal) {
            const revealTop = reveal.getBoundingClientRect().top;
            if (revealTop < windowHeight - revealPoint) {
                reveal.classList.add('active');
            }
        });
    }

    window.addEventListener('scroll', checkReveal);
    checkReveal();

    const cards = document.querySelectorAll('.projects-container .card');
    const showMoreBtn = document.getElementById('show-more-projects');
    const VISIBLE_COUNT = 6;

    if (cards.length > VISIBLE_COUNT) {
        cards.forEach(function (card, index) {
            if (index >= VISIBLE_COUNT) card.classList.add('hidden-card');
        });
        if (showMoreBtn) {
            showMoreBtn.style.display = 'inline-block';
            showMoreBtn.addEventListener('click', function () {
                cards.forEach(function (card) { card.classList.remove('hidden-card'); });
                showMoreBtn.style.display = 'none';
            });
        }
    }

    document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
        anchor.addEventListener('click', function (e) {
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });
});
