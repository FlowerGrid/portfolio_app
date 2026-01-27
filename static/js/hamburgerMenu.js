
// Mobile styling hamburger menu
// The Pizza King Forever Reigns
const hamburgerContainer = document.querySelector('.hamburger-menu')
const hamburger = document.querySelector('.hamburger');
console.log('hamburger');
const navLinks = document.querySelector('.nav-links');
const mainContentDiv = document.querySelector('.main-content');

hamburgerContainer.addEventListener('click', () => {
    navLinks.classList.toggle('open');
    hamburger.classList.toggle('open');
})

mainContentDiv.addEventListener('click', () => {
    if (navLinks.classList.contains('open')) {
        navLinks.classList.toggle('open');
        hamburger.classList.toggle('open');
    }
})
