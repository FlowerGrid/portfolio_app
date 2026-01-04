// Open Links in a new tab
const pageContent = document.querySelector('.page-content');
const links = pageContent.querySelectorAll('a');
links.forEach(link => {
    if (!link.classList.contains('button-styles')){
        link.setAttribute('target', '_blank');
        link.setAttribute('rel', 'noopener noreferrer');
    }

})