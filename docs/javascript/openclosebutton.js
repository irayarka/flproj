document.querySelector('.grid-container .menu-icon').addEventListener('click', function () {
    document.querySelector('.sidenav').classList.add('active');
    document.querySelector('.grid-container .header').classList.add('active');
    document.querySelector('.main').classList.add('active');
});
document.querySelector('.sidenav__close-icon').addEventListener('click', function () {
    document.querySelector('.sidenav').classList.remove('active');
    document.querySelector('.grid-container .header').classList.remove('active');
    document.querySelector('.main').classList.remove('active');
});
