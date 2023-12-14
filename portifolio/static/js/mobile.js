document.addEventListener('DOMContentLoaded', function () {
    const toggleBtn = document.getElementById('menu');
    const navegationBar = document.getElementById('bar');
    const menuItems = document.querySelectorAll('#bar a');

    toggleBtn.addEventListener('click', function (event) {
        event.stopPropagation();
        navegationBar.classList.toggle('active');
    });

    document.addEventListener('click', function (event) {
        if (!navegationBar.contains(event.target) && event.target !== toggleBtn) {
            navegationBar.classList.remove('active');
        }
    });

    menuItems.forEach(function (menuItem) {
        menuItem.addEventListener('click', function () {
            navegationBar.classList.remove('active');
        });
    });
});